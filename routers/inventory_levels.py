from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
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
    collection: AsyncIOMotorClient = Depends(get_db_collection),
    branch_id: Optional[int] = Query(None, description="Filter by Branch ID")
):
    """
    Retrieves current inventory levels for all products, optionally filtered by branch.
    """
    query = {}
    if branch_id is not None:
        query["branch_id"] = branch_id

    data = await collection.find(query).to_list(length=None)

    results = calculate_inventory_levels(data)
    for item in results:
        item["description"] = (
            f"Product {item.get('product_name', 'N/A')} (ID: {item.get('product_id', 'N/A')}) "
            f"Initial Inventory: {item.get('initial_inventory', 0)}, "
            f"Total Sold: {item.get('quantity_sold_total', 0)}, "
            f"Current Inventory: {item.get('current_inventory', 0)}."
        )
        if branch_id is not None:
            item["description"] += f" (Branch ID: {branch_id})"
    return results
