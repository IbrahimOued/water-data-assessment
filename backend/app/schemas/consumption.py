from datetime import datetime
from pydantic import BaseModel

class Consumption(BaseModel):
    reading_id: int
    point_id: int
    meter_type_id: int
    connection_type_id: int
    status_id: int
    recorder_id: int
    reading_date: datetime
    meter_index: int
    revenue_fcfa: float
    notes: str

    class Config:
        from_attributes = True

class ConsumptionResponse(BaseModel):
    reading_date: datetime
    meter_index: float