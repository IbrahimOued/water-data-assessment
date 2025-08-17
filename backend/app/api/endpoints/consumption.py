from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session
from app.schemas.consumption import Consumption
from app.crud.consumption import get_consumptions
from app.db.session import get_db

router = APIRouter()

# Consumption
@router.get("/", response_model=List[Consumption])
def read_consumptions(
    db: Session = Depends(get_db),
    point_id: Optional[int] = Query(None, description="Filter by point_id"),
    start_date: Optional[date] = Query(None, description="Filter by start date (inclusive)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (inclusive)"),
    limit: Optional[int] = Query(100, description="Limit the number of results"),
):
    return get_consumptions(db, point_id=point_id, start_date=start_date, end_date=end_date, limit=limit)
