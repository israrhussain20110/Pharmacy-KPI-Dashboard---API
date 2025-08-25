from fastapi import APIRouter, Depends
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_collection
from services.calculations import calculate_total_sales_value
from datetime import datetime # Import datetime

router = APIRouter(
    prefix="/sales-value",
    tags=["Sales Value"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=Dict[str, Any])
async def get_total_sales_value(
    collection: AsyncIOMotorClient = Depends(get_db_collection)
):
    """
    Retrieves the total sales value.
    """
    data = await collection.find().to_list(length=None)
    # Convert date strings back to datetime objects if necessary for calculations
    for item in data:
        if isinstance(item.get('Date'), str):
            item['Date'] = datetime.fromisoformat(item['Date'].split('T')[0])
        if isinstance(item.get('Expiration_Date'), str):
            item['Expiration_Date'] = datetime.fromisoformat(item['Expiration_Date'].split('T')[0])

    result = calculate_total_sales_value(data)
    result["description"] = f"Total sales value: {result.get('total_sales_value', 0):.2f}."
    return result
