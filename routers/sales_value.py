from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
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
    collection: AsyncIOMotorClient = Depends(get_db_collection),
    branch_id: Optional[int] = Query(None, description="Filter by Branch ID")
):
    """
    Retrieves the total sales value, optionally filtered by branch.
    """
    query = {}
    if branch_id is not None:
        query["branch_id"] = branch_id

    data = await collection.find(query).to_list(length=None)

    result = calculate_total_sales_value(data)
    result["description"] = f"Total sales value: {result.get('total_sales_value', 0):.2f}."
    if branch_id is not None:
        result["description"] += f" (Branch ID: {branch_id})"
    return result
