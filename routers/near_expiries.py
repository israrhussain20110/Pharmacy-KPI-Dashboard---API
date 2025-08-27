from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
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
    collection: AsyncIOMotorClient = Depends(get_db_collection),
    branch_id: Optional[int] = Query(None, description="Filter by Branch ID")
):
    """
    Retrieves products that are near their expiration date, optionally filtered by branch.
    """
    query = {}
    if branch_id is not None:
        query["branch_id"] = branch_id

    data = await collection.find(query).to_list(length=None)

    results = calculate_near_expiries(data, days_threshold)
    for item in results:
        item["description"] = (
            f"Product {item.get('product_name', 'N/A')} (ID: {item.get('product_id', 'N/A')}) "
            f"expires on {item.get('expiration_date', datetime.min).strftime('%Y-%m-%d')} "
            f"(Days to expiry: {item.get('days_to_expiry', 'N/A')})."
        )
        if branch_id is not None:
            item["description"] += f" (Branch ID: {branch_id})"
    return results
