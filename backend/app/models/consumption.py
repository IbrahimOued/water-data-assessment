from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey, UniqueConstraint
from app.db.base import Base

class Consumption(Base):
    __tablename__ = "meter_readings"
    reading_id = Column(Integer, primary_key=True, index=True)
    # Foreign keys to dimensions
    point_id = Column(Integer, ForeignKey("points.point_id"), nullable=False)
    meter_type_id = Column(Integer, ForeignKey("meter_types.meter_type_id"), nullable=False)
    connection_type_id = Column(Integer, ForeignKey("connection_types.connection_type_id"), nullable=False)
    status_id = Column(Integer, ForeignKey("statuses.status_id"), nullable=False)
    recorder_id = Column(Integer, ForeignKey("recorders.recorder_id"), nullable=False)
    # Attributes of the reading
    reading_date = Column(DateTime, nullable=False)
    meter_index = Column(Integer, nullable=False)
    revenue_fcfa = Column(Float, nullable=False)
    notes = Column(String, nullable=True)
    __table_args__ = (
        UniqueConstraint("point_id", "reading_date", name="uq_point_reading_date"),
        {"schema": "water_metering"}
    )
