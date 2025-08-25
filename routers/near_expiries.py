from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_collection
from services.calculations import calculate_near_expiries
from datetime import datetime # Import datetime

router = APIRouter(
    prefix="/near-expiries",
    tags=["Near-Expiries"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_near_expiries(
    days_threshold: int = 30,
    collection: AsyncIOMotorClient = Depends(get_db_collection)
):
    """
    Retrieves products that are near their expiration date.
    """
    data = await collection.find().to_list(length=None)
    # Convert date strings back to datetime objects if necessary for calculations
    for item in data:
        if isinstance(item.get('Date'), str):
            item['Date'] = datetime.fromisoformat(item['Date'].split('T')[0])
        if isinstance(item.get('Expiration_Date'), str):
            item['Expiration_Date'] = datetime.fromisoformat(item['Expiration_Date'].split('T')[0])

    results = calculate_near_expiries(data, days_threshold)
    for item in results:
        item["description"] = (
            f"Product {item.get('product_name', 'N/A')} (ID: {item.get('product_id', 'N/A')}) "
            f"expires on {item.get('expiration_date', datetime.min).strftime('%Y-%m-%d')} "
            f"(Days to expiry: {item.get('days_to_expiry', 'N/A')})."
        )
    return results
