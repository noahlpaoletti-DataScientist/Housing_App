from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas import ComparableResponse, PropertyLookupResponse
from app.db.models import Property
from app.db.session import get_db
from app.services.comparable_service import get_adjusted_comparables
from app.services.property_lookup_service import get_property_by_address
from app.services.report_service import build_property_report

router = APIRouter(tags=["property"])


@router.get("/property/lookup", response_model=PropertyLookupResponse)
def property_lookup(address: str = Query(...), db: Session = Depends(get_db)):
    property_record = get_property_by_address(db, address)
    if property_record is None:
        return PropertyLookupResponse(
            input_address=address,
            matched_property=None,
            formula_explanation="No matching property was found in the seeded mock dataset.",
        )
    return build_property_report(db, property_record)


@router.get("/property/{property_id}/comparables", response_model=list[ComparableResponse])
def property_comparables(property_id: int, db: Session = Depends(get_db)):
    property_record = db.query(Property).filter(Property.id == property_id).one_or_none()
    if property_record is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return get_adjusted_comparables(db, property_record)["comparables"]
