from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import InvestmentAnalysisRequest, InvestmentAnalysisResponse
from app.db.session import get_db
from app.services.investment_service import analyze_investment

router = APIRouter(tags=["investment"])


@router.post("/investment/analyze", response_model=InvestmentAnalysisResponse)
def analyze(payload: InvestmentAnalysisRequest, db: Session = Depends(get_db)):
    return analyze_investment(
        db,
        payload.model_dump(),
        property_id=payload.property_id,
        persist=False,
    )
