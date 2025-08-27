from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
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
    collection: AsyncIOMotorClient = Depends(get_db_collection),
    branch_id: Optional[int] = Query(None, description="Filter by Branch ID")
):
    """
    Retrieves the top selling products by sales value, optionally filtered by branch.
    """
    query = {}
    if branch_id is not None:
        query["branch_id"] = branch_id

    data = await collection.find(query).to_list(length=None)

    results = calculate_top_sellers(data, top_n)
    for item in results:
        item["description"] = (
            f"Product {item.get('product_name', 'N/A')} (ID: {item.get('product_id', 'N/A')}) "
            f"had a total sales value of {item.get('total_sales_value', 0):.2f}."
        )
        if branch_id is not None:
            item["description"] += f" (Branch ID: {branch_id})"
    return results
