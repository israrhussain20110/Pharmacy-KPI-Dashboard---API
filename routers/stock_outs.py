from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_collection
from services.calculations import calculate_stock_outs
from datetime import date

router = APIRouter(
    prefix="/stock-outs",
    tags=["Stock-Outs"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_stock_outs(
    collection: AsyncIOMotorClient = Depends(get_db_collection)
):
    """
    Retrieves records of stock-out events.
    """
    data = await collection.find().to_list(length=None)
    # Convert date strings back to date objects if necessary for calculations
    for item in data:
        if isinstance(item.get('date'), str):
            item['date'] = date.fromisoformat(item['date'].split('T')[0])
        if isinstance(item.get('expiration_date'), str):
            item['expiration_date'] = date.fromisoformat(item['expiration_date'].split('T')[0])

    return calculate_stock_outs(data)
