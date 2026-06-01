from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import PropertyLookupResponse
from app.db.models import Property
from app.db.session import get_db
from app.services.report_service import build_property_report

router = APIRouter(tags=["report"])


@router.get("/report/property/{property_id}", response_model=PropertyLookupResponse)
def property_report(property_id: int, db: Session = Depends(get_db)):
    property_record = db.query(Property).filter(Property.id == property_id).one_or_none()
    if property_record is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return build_property_report(db, property_record)
