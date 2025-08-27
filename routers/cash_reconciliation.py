from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_collection
from services.calculations import calculate_cash_reconciliation
from datetime import datetime # Import datetime

router = APIRouter(
    prefix="/cash-reconciliation",
    tags=["Cash Reconciliation"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=Dict[str, Any])
async def get_cash_reconciliation(
    collection: AsyncIOMotorClient = Depends(get_db_collection),
    branch_id: Optional[int] = Query(None, description="Filter by Branch ID")
):
    """
    Compares total sales value with total cash received, optionally filtered by branch.
    """
    query = {}
    if branch_id is not None:
        query["branch_id"] = branch_id

    data = await collection.find(query).to_list(length=None)

    result = calculate_cash_reconciliation(data)
    result["description"] = (
        f"Total sales: {result.get('total_sales_value', 0):.2f}, "
        f"Total cash received: {result.get('total_cash_received', 0):.2f}, "
        f"Discrepancy: {result.get('discrepancy', 0):.2f}."
    )
    if branch_id is not None:
        result["description"] += f" (Branch ID: {branch_id})"
    return result
