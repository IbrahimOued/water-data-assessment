-- ------------- 0.  Create a schema -----------------------------------
CREATE SCHEMA IF NOT EXISTS water_metering;
SET search_path = water_metering, public;

-- ------------- 1.  PostGIS extension (for spatial indexes) ----------

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- ------------- 2.  Dimension tables ----------------------------------
-- 2a.  Points (location of a meter)
CREATE TABLE points (
    point_id        BIGSERIAL PRIMARY KEY,
    point_name      TEXT    NOT NULL,
    commune         TEXT    NOT NULL,
    village         TEXT    NOT NULL,
    latitude        DOUBLE PRECISION NOT NULL,
    longitude       DOUBLE PRECISION NOT NULL,
    installation_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    -- For spatial indexing
    geom            GEOMETRY(Point,4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude, latitude),4326)) STORED
);
-- Spatial index
CREATE INDEX points_geom_idx ON points USING GIST (geom);

-- 2b.  Meter types
CREATE TABLE meter_types (
    meter_type_id   BIGSERIAL PRIMARY KEY,
    meter_type_name TEXT UNIQUE NOT NULL
);

-- 2c.  Connection types
CREATE TABLE connection_types (
    connection_type_id   BIGSERIAL PRIMARY KEY,
    connection_type_name TEXT UNIQUE NOT NULL
);

-- 2d.  Status
CREATE TABLE statuses (
    status_id   BIGSERIAL PRIMARY KEY,
    status_name TEXT UNIQUE NOT NULL
);

-- 2e.  Recorders (who logged the reading)
CREATE TABLE recorders (
    recorder_id   BIGSERIAL PRIMARY KEY,
    recorder_name TEXT UNIQUE NOT NULL
);

-- ------------- 3.  Fact table ---------------------------------------
CREATE TABLE meter_readings (
    reading_id        BIGSERIAL PRIMARY KEY,

    -- Foreign keys to dimensions
    point_id          BIGINT NOT NULL REFERENCES points(point_id),
    meter_type_id     BIGINT NOT NULL REFERENCES meter_types(meter_type_id),
    connection_type_id BIGINT NOT NULL REFERENCES connection_types(connection_type_id),
    status_id         BIGINT NOT NULL REFERENCES statuses(status_id),
    recorder_id       BIGINT NOT NULL REFERENCES recorders(recorder_id),

    -- Attributes of the reading
    reading_date      TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    meter_index       BIGINT NOT NULL,
    revenue_fcfa      DOUBLE PRECISION,
    notes             TEXT,

    -- A natural key that guarantees uniqueness per point per reading_date
    UNIQUE (point_id, reading_date)
);

-- Indexes that help typical queries
CREATE INDEX meter_readings_point_idx ON meter_readings(point_id);
CREATE INDEX meter_readings_meter_index_idx ON meter_readings(meter_index);
CREATE INDEX meter_readings_reading_date_idx ON meter_readings(reading_date);
