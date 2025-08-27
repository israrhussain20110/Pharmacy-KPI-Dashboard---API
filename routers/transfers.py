from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import get_db_client # Use get_db_client to get the client and then access a different collection
from pydantic import BaseModel
from datetime import datetime
from services.calculations import calculate_transfer_volume_by_branch, calculate_transfer_value_by_branch

router = APIRouter(
    prefix="/transfers",
    tags=["Inter-Branch Transfers"],
    responses={404: {"description": "Not found"}},
)

class Transfer(BaseModel):
    from_branch: int
    to_branch: int
    product_id: str
    quantity: int
    date: datetime = datetime.now()
    cost: float

@router.post("/", status_code=201)
async def log_transfer(
    transfer: Transfer,
    db_client: AsyncIOMotorClient = Depends(get_db_client)
):
    """
    Logs a new inter-branch transfer.
    """
    transfers_collection = db_client["pharmacy_kpi_db"]["transfers"] # Assuming 'pharmacy_kpi_db' is the DB name
    transfer_dict = transfer.dict()
    result = await transfers_collection.insert_one(transfer_dict)
    return {"message": "Transfer logged successfully", "id": str(result.inserted_id)}

@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_transfers(
    db_client: AsyncIOMotorClient = Depends(get_db_client)
):
    """
    Retrieves all logged inter-branch transfers.
    """
    transfers_collection = db_client["pharmacy_kpi_db"]["transfers"]
    transfers = await transfers_collection.find().to_list(length=None)
    for transfer in transfers:
        transfer["_id"] = str(transfer["_id"]) # Convert ObjectId to string
    return transfers

@router.get("/summary", response_model=Dict[str, Any])
async def get_transfers_summary(
    db_client: AsyncIOMotorClient = Depends(get_db_client)
):
    """
    Retrieves a summary of inter-branch transfers, including volume and value by branch.
    """
    transfers_collection = db_client["pharmacy_kpi_db"]["transfers"]
    transfers_data = await transfers_collection.find().to_list(length=None)

    transfer_volume = calculate_transfer_volume_by_branch(transfers_data)
    transfer_value = calculate_transfer_value_by_branch(transfers_data)

    return {
        "transfer_volume_by_branch": transfer_volume,
        "transfer_value_by_branch": transfer_value,
    }
