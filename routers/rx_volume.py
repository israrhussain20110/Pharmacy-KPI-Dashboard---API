from fastapi import APIRouter, Depends
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_collection
from services.calculations import calculate_rx_volume
from datetime import datetime # Import datetime

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
    # Convert date strings back to datetime objects if necessary for calculations
    for item in data:
        if isinstance(item.get('Date'), str):
            item['Date'] = datetime.fromisoformat(item['Date'].split('T')[0])
        if isinstance(item.get('Expiration_Date'), str):
            item['Expiration_Date'] = datetime.fromisoformat(item['Expiration_Date'].split('T')[0])

    result = calculate_rx_volume(data)
    result["description"] = f"Total Rx volume: {result.get('total_rx_volume', 0):.2f}."
    return result
