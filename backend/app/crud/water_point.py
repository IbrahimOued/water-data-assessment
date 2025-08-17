from sqlalchemy.orm import Session
from app.models.water_point import WaterPoint
from app.models.consumption import Consumption

def get_water_points(db: Session):
    return db.query(WaterPoint).all()

def get_water_point_consumption(db: Session, id: int):
    return db.query(Consumption).filter(Consumption.point_id == id).all()
