from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
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
    collection: AsyncIOMotorClient = Depends(get_db_collection),
    branch_id: Optional[int] = Query(None, description="Filter by Branch ID")
):
    """
    Retrieves the total prescription (Rx) volume, optionally filtered by branch.
    """
    query = {}
    if branch_id is not None:
        query["branch_id"] = branch_id

    data = await collection.find(query).to_list(length=None)

    result = calculate_rx_volume(data)
    result["description"] = f"Total Rx volume: {result.get('total_rx_volume', 0):.2f}."
    if branch_id is not None:
        result["description"] += f" (Branch ID: {branch_id})"
    return result
