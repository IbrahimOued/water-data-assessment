from datetime import date
from typing import List, List, Optional
from sqlalchemy.orm import Session
from app.models.consumption import Consumption

# /consumptions/ -> Returns up to 100 consumptions.
# /consumptions/?point_id=5 -> Returns consumptions for point_id 5.
# /consumptions/?start_date=2025-01-01&end_date=2025-01-31 -> Returns consumptions between January 1 and January 31, 2025.
# /consumptions/?point_id=5&limit=10 -> Returns up to 10 consumptions for point_id 5.
def get_consumptions(
    db: Session,
    point_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 100,
) -> List[Consumption]:
    query = db.query(Consumption)
    # Apply filters based on the provided parameters
    if point_id is not None:
        query = query.filter(Consumption.point_id == point_id)
    if start_date is not None:
        query = query.filter(Consumption.reading_date >= start_date)
    if end_date is not None:
        query = query.filter(Consumption.reading_date <= end_date)

    return query.limit(limit).all()
