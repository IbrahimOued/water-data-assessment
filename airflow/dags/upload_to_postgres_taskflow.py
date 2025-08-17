# dags/upload_water_metering_data.py
import os
import re
from datetime import datetime

import pandas as pd
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

# --- Environment Configuration ---
# The DAG will use the default postgres connection 'postgres_default'.
LOCAL_DATA_FOLDER = os.getenv('LOCAL_DATA_FOLDER', '/opt/airflow/dataset')
POSTGRES_CONN_ID = os.getenv('POSTGRES_CONN_ID', 'postgres_default')
TARGET_SCHEMA = os.getenv('DB_TARGET_SCHEMA', 'water_metering')

def sanitize_table_name(file_name: str) -> str:
    """
    Cleans a file name to create a valid, safe SQL table name.
    - Removes .csv extension
    - Converts to lowercase
    - Replaces spaces and hyphens with underscores
    - Removes any other non-alphanumeric characters (except underscores)
    """
    base_name = file_name.lower().replace('.csv', '')
    sane_name = re.sub(r'[^a-z0-9_]+', '_', base_name)
    return re.sub(r'^[^a-z]+', '', sane_name)

@dag(
    dag_id='upload_water_metering_to_postgres',
    start_date=datetime(2025, 8, 1),
    schedule="@once",
    catchup=False,
    tags=['postgres', 'water-metering'],
    doc_md="DAG to process CSV files with merged headers and upload to the water_metering schema in PostgreSQL."
)
def upload_water_metering_to_postgres():
    @task()
    def retrieve_csv_file() -> str:
        """There should be at least one csv file"""
        print(f"Searching for the CSV file in: {LOCAL_DATA_FOLDER}")
        # Look for the first CSV file found
        for file in os.listdir(LOCAL_DATA_FOLDER):
            if file.endswith('.csv'):
                print(f"Found CSV file: {file}")
                return file
            # If we found a CSV file, we can stop searching
        print("No CSV file found.")
        return None


    @task(do_xcom_push=True)
    def process_and_clean_file(file_name: str, **context):
        """
        Reads a CSV file, processes it, and returns a cleaned DataFrame.
        """
        file_path = os.path.join(LOCAL_DATA_FOLDER, file_name)
        print(f"Processing file: {file_path}")
        
        df = pd.read_csv(file_path)
        # Split the data into columns
        df = df.iloc[:, 0].str.split(',', expand=True).rename(columns={
            0: 'point_name',
            1: 'commune',
            2: 'village',
            3: 'latitude',
            4: 'longitude',
            5: 'installation_date',
            6: 'meter_type',
            7: 'connection_type',
            8: 'status',
            9: 'reading_date',
            10: 'meter_index',
            11: 'revenue_fcfa',
            12: 'recorded_by',
            13: 'notes'
        })

        # point_name,commune,village,latitude,longitude,installation_date,meter_type,connection_type,status,reading_date,meter_index,revenue_fcfa,recorded_by,notes'
        dtype_map = {
            'point_name': 'category',
            'commune': 'category',
            'village': 'category',
            'latitude': 'float64',
            'longitude': 'float64',
            'installation_date': 'datetime64[ns]',
            'meter_type': 'category',
            'connection_type': 'category',
            'status': 'category',
            'reading_date': 'datetime64[ns]',
            'meter_index': 'int64',
            'revenue_fcfa': 'float64',
            'recorded_by': 'category',
            'notes': 'category'
        }

        # Convert columns to appropriate dtypes
        for column, dtype in dtype_map.items():
            df[column] = df[column].astype(dtype)
            
        # push to XCOM
        context['ti'].xcom_push(key='clean_df', value=df)

    @task()
    def upsert_dimensions_and_fact(**context):
        from sqlalchemy import text
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        engine = hook.get_sqlalchemy_engine()

        df = context['ti'].xcom_pull(task_ids='process_and_clean_file', key='clean_df')

        with engine.begin() as conn:
            # --- DIMENSIONS ---
            def get_or_create_id(table, id_col, name_col, value):
                result = conn.execute(
                    text(f"SELECT {id_col} FROM {TARGET_SCHEMA}.{table} WHERE {name_col} = :val"),
                    {"val": value}
                ).fetchone()
                if result:
                    return result[0]
                inserted = conn.execute(
                    text(f"INSERT INTO {TARGET_SCHEMA}.{table} ({name_col}) VALUES (:val) RETURNING {id_col}"),
                    {"val": value}
                ).fetchone()
                return inserted[0]

            # --- UPSERT LOGIC ---
            for _, row in df.iterrows():
                # Points
                point_id = conn.execute(
                    text(f"""
                    SELECT point_id FROM {TARGET_SCHEMA}.points
                    WHERE point_name = :pname AND latitude = :lat AND longitude = :lon
                    """),
                    {"pname": row.point_name, "lat": row.latitude, "lon": row.longitude}
                ).fetchone()
                if not point_id:
                    point_id = conn.execute(
                        text(f"""
                        INSERT INTO {TARGET_SCHEMA}.points
                        (point_name, commune, village, latitude, longitude, installation_date)
                        VALUES (:pname, :commune, :village, :lat, :lon, :inst)
                        RETURNING point_id
                        """),
                        {
                            "pname": row.point_name, "commune": row.commune, "village": row.village,
                            "lat": row.latitude, "lon": row.longitude, "inst": row.installation_date
                        }
                    ).fetchone()
                point_id = point_id[0]

                # Other dimensions
                meter_type_id = get_or_create_id("meter_types", "meter_type_id", "meter_type_name", row.meter_type)
                connection_type_id = get_or_create_id("connection_types", "connection_type_id", "connection_type_name", row.connection_type)
                status_id = get_or_create_id("statuses", "status_id", "status_name", row.status)
                recorder_id = get_or_create_id("recorders", "recorder_id", "recorder_name", row.recorded_by)

                # Fact table insert/update
                conn.execute(
                    text(f"""
                    INSERT INTO {TARGET_SCHEMA}.meter_readings
                    (point_id, meter_type_id, connection_type_id, status_id, recorder_id,
                    reading_date, meter_index, revenue_fcfa, notes)
                    VALUES (:pid, :mtid, :ctid, :sid, :rid, :rdate, :mindex, :revenue, :notes)
                    ON CONFLICT (point_id, reading_date) DO UPDATE
                    SET meter_index = EXCLUDED.meter_index,
                        revenue_fcfa = EXCLUDED.revenue_fcfa,
                        notes = EXCLUDED.notes
                    """),
                    {
                        "pid": point_id, "mtid": meter_type_id, "ctid": connection_type_id,
                        "sid": status_id, "rid": recorder_id,
                        "rdate": row.reading_date, "mindex": row.meter_index,
                        "revenue": row.revenue_fcfa, "notes": row.notes
                    }
                )


    # Create the task dependency chain
    csv_file = retrieve_csv_file()
    process_and_clean_file(file_name=csv_file) >> upsert_dimensions_and_fact()

upload_water_metering_to_postgres()