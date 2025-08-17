from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.water_point import WaterPoint
from app.schemas.consumption import ConsumptionResponse
from app.crud.water_point import get_water_points, get_water_point_consumption
from app.db.session import get_db

router = APIRouter()

# Water Points
@router.get("/", response_model=list[WaterPoint])
def read_water_points(db: Session = Depends(get_db)):
    return get_water_points(db)

@router.get("/{id}/consumption", response_model=list[ConsumptionResponse])
def read_water_point_consumption(id: int, db: Session = Depends(get_db)):
    return get_water_point_consumption(db, id)
