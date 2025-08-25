from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_collection
from services.calculations import calculate_inventory_levels
from datetime import datetime # Import datetime

router = APIRouter(
    prefix="/inventory-levels",
    tags=["Inventory Levels"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_inventory_levels(
    collection: AsyncIOMotorClient = Depends(get_db_collection)
):
    """
    Retrieves current inventory levels for all products.
    """
    data = await collection.find().to_list(length=None)
    # Convert date strings back to datetime objects if necessary for calculations
    for item in data:
        if isinstance(item.get('Date'), str):
            item['Date'] = datetime.fromisoformat(item['Date'].split('T')[0])
        if isinstance(item.get('Expiration_Date'), str):
            item['Expiration_Date'] = datetime.fromisoformat(item['Expiration_Date'].split('T')[0])

    results = calculate_inventory_levels(data)
    for item in results:
        item["description"] = (
            f"Product {item.get('product_name', 'N/A')} (ID: {item.get('product_id', 'N/A')}) "
            f"Initial Inventory: {item.get('initial_inventory', 0)}, "
            f"Total Sold: {item.get('quantity_sold_total', 0)}, "
            f"Current Inventory: {item.get('current_inventory', 0)}."
        )
    return results
