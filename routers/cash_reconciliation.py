from fastapi import APIRouter, Depends
from typing import Dict, Any
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
    collection: AsyncIOMotorClient = Depends(get_db_collection)
):
    """
    Compares total sales value with total cash received.
    """
    data = await collection.find().to_list(length=None)
    # Convert date strings back to datetime objects if necessary for calculations
    for item in data:
        if isinstance(item.get('Date'), str):
            item['Date'] = datetime.fromisoformat(item['Date'].split('T')[0])
        if isinstance(item.get('Expiration_Date'), str):
            item['Expiration_Date'] = datetime.fromisoformat(item['Expiration_Date'].split('T')[0])

    result = calculate_cash_reconciliation(data)
    result["description"] = (
        f"Total sales: {result.get('total_sales_value', 0):.2f}, "
        f"Total cash received: {result.get('total_cash_received', 0):.2f}, "
        f"Discrepancy: {result.get('discrepancy', 0):.2f}."
    )
    return result
