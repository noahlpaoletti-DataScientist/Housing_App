from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import RenovationEstimateRequest, RenovationEstimateResponse
from app.db.session import get_db
from app.services.renovation_service import create_renovation_estimate

router = APIRouter(tags=["renovation"])


@router.post("/renovation/estimate", response_model=RenovationEstimateResponse)
def estimate_renovation(payload: RenovationEstimateRequest, db: Session = Depends(get_db)):
    return create_renovation_estimate(
        db,
        renovation_type=payload.renovation_type,
        inputs=payload.inputs,
        property_id=payload.property_id,
        persist=False,
    )
