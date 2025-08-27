from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_collection
from services.calculations import calculate_stock_outs
from datetime import datetime # Import datetime

router = APIRouter(
    prefix="/stock-outs",
    tags=["Stock-Outs"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_stock_outs(
    collection: AsyncIOMotorClient = Depends(get_db_collection),
    branch_id: Optional[int] = Query(None, description="Filter by Branch ID")
):
    """
    Retrieves records of stock-out events, optionally filtered by branch.
    """
    query = {}
    if branch_id is not None:
        query["branch_id"] = branch_id

    data = await collection.find(query).to_list(length=None)
    # Convert date strings back to datetime objects if necessary for calculations
    for item in data:
        if isinstance(item.get('Date'), str):
            item['Date'] = datetime.fromisoformat(item['Date'].split('T')[0])
        if isinstance(item.get('Expiration_Date'), str):
            item['Expiration_Date'] = datetime.fromisoformat(item['Expiration_Date'].split('T')[0])

    results = calculate_stock_outs(data)
    for item in results:
        item["description"] = (
            f"Stock-out for {item.get('product_name', 'N/A')} (ID: {item.get('product_id', 'N/A')}) "
            f"on {item.get('date', datetime.min).strftime('%Y-%m-%d')}. "
            f"Quantity sold during stock-out: {item.get('quantity_sold_during_stock_out', 0)}."
        )
        if branch_id is not None:
            item["description"] += f" (Branch ID: {branch_id})"
    return results
