from fastapi import APIRouter, Depends
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_collection
from services.calculations import calculate_rx_volume
from datetime import date

router = APIRouter(
    prefix="/rx-volume",
    tags=["Rx Volume"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=Dict[str, Any])
async def get_rx_volume(
    collection: AsyncIOMotorClient = Depends(get_db_collection)
):
    """
    Retrieves the total prescription (Rx) volume.
    """
    data = await collection.find().to_list(length=None)
    # Convert date strings back to date objects if necessary for calculations
    for item in data:
        if isinstance(item.get('date'), str):
            item['date'] = date.fromisoformat(item['date'].split('T')[0])
        if isinstance(item.get('expiration_date'), str):
            item['expiration_date'] = date.fromisoformat(item['expiration_date'].split('T')[0])

    return calculate_rx_volume(data)
