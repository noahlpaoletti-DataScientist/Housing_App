from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import FormulaResponse, PropertyLookupResponse
from app.db.models import Property
from app.db.session import get_db
from app.services.valuation_service import build_property_valuation

router = APIRouter(tags=["valuation"])


def _get_property_or_404(db: Session, property_id: int) -> Property:
    property_record = db.query(Property).filter(Property.id == property_id).one_or_none()
    if property_record is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_record


@router.get("/property/{property_id}/valuation", response_model=PropertyLookupResponse)
def get_property_valuation(property_id: int, db: Session = Depends(get_db)):
    property_record = _get_property_or_404(db, property_id)
    valuation = build_property_valuation(db, property_record)
    return {
        "input_address": property_record.address,
        "matched_property": {"id": property_record.id, "address": property_record.address},
        "estimated_value": valuation["estimated_value"],
        "low_estimate": valuation["low_estimate"],
        "high_estimate": valuation["high_estimate"],
        "confidence_score": valuation["confidence_score"],
        "confidence_explanation": valuation["confidence_explanation"],
        "valuation_breakdown": valuation["valuation_breakdown"],
        "formula_explanation": valuation["formula_explanation"],
        "comparable_sales": valuation["comparable_sales"],
        "renovation_scenarios": [],
        "investment_summary": {},
        "market_trends": valuation["market_trends"],
        "data_sources_used": valuation["data_sources_used"],
        "valuation_components": valuation["components"],
    }


@router.get("/property/{property_id}/formula", response_model=FormulaResponse)
def get_property_formula(property_id: int, db: Session = Depends(get_db)):
    property_record = _get_property_or_404(db, property_id)
    valuation = build_property_valuation(db, property_record)
    return {
        "property_id": property_record.id,
        "adjusted_weights": valuation["valuation_breakdown"],
        "components": valuation["components"],
        "formula_explanation": valuation["formula_explanation"],
    }
