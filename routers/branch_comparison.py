from fastapi import APIRouter, Depends
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_collection
from services.calculations import (
    calculate_sales_by_branch,
    calculate_inventory_turns_by_branch,
    calculate_service_level_by_branch,
)

router = APIRouter(
    prefix="/branches",
    tags=["Branch Comparison"],
    responses={404: {"description": "Not found"}},
)

@router.get("/compare", response_model=Dict[str, Any])
async def compare_branches(
    collection: AsyncIOMotorClient = Depends(get_db_collection),
):
    """
    Compares key performance indicators (KPIs) across all branches.
    """
    data = await collection.find({}).to_list(length=None)

    sales_by_branch = calculate_sales_by_branch(data)
    inventory_turns_by_branch = calculate_inventory_turns_by_branch(data)
    service_level_by_branch = calculate_service_level_by_branch(data)

    comparison_data = {
        "sales_by_branch": sales_by_branch,
        "inventory_turns_by_branch": inventory_turns_by_branch,
        "service_level_by_branch": service_level_by_branch,
    }

    return comparison_data
