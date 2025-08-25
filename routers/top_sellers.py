from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_collection
from services.calculations import calculate_top_sellers
from datetime import datetime # Import datetime

router = APIRouter(
    prefix="/top-sellers",
    tags=["Top Sellers"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_top_sellers(
    top_n: int = 5,
    collection: AsyncIOMotorClient = Depends(get_db_collection)
):
    """
    Retrieves the top selling products by sales value.
    """
    data = await collection.find().to_list(length=None)
    # Convert date strings back to datetime objects if necessary for calculations
    for item in data:
        if isinstance(item.get('Date'), str):
            item['Date'] = datetime.fromisoformat(item['Date'].split('T')[0])
        if isinstance(item.get('Expiration_Date'), str):
            item['Expiration_Date'] = datetime.fromisoformat(item['Expiration_Date'].split('T')[0])

    results = calculate_top_sellers(data, top_n)
    for item in results:
        item["description"] = (
            f"Product {item.get('product_name', 'N/A')} (ID: {item.get('product_id', 'N/A')}) "
            f"had a total sales value of {item.get('total_sales_value', 0):.2f}."
        )
    return results
