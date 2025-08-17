export interface Consumption {
  reading_id: number;
  point_id: number;
  meter_type_id: number;
  connection_type_id: number;
  status_id: number;
  recorder_id: number;
  reading_date: string;   // datetime as ISO string
  meter_index: number;
  revenue_fcfa: number;
  notes: string;
}

export interface ConsumptionResponse {
  reading_date: string;
  meter_index: number;
}

export interface WaterPoint {
  point_id: number;
  point_name: string;
  commune: string;
  village: string;
  latitude: number;
  longitude: number;
  installation_date: string;
  geom: string;
}
