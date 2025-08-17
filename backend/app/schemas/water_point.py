from datetime import datetime
from pydantic import BaseModel

class WaterPoint(BaseModel):
    point_id: int
    point_name: str
    commune: str
    village: str
    latitude: float
    longitude: float
    installation_date: datetime
    geom: str

    class Config:
        from_attributes = True
