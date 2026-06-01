from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import MarketTrendResponse
from app.db.session import get_db
from app.services.market_service import get_market_trend, serialize_market_trend

router = APIRouter(tags=["market"])


@router.get("/market/trends", response_model=MarketTrendResponse)
def market_trends(zip_code: str, db: Session = Depends(get_db)):
    return serialize_market_trend(get_market_trend(db, zip_code))
