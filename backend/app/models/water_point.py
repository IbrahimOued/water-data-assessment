from sqlalchemy import Column, DateTime, Float, Integer, String
from app.db.base import Base

class WaterPoint(Base):
    __tablename__ = "points"
    __table_args__ = {"schema": "water_metering"}
    point_id = Column(Integer, primary_key=True, index=True)
    point_name = Column(String, nullable=False)
    commune = Column(String, nullable=False)
    village = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    installation_date = Column(DateTime, nullable=False)
    geom = Column(String, nullable=False)  # Assuming geom is stored as a string representation of the geometry
