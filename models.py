from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.is_instance_schema(ObjectId),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

class KPIData(BaseModel):
    Date: datetime
    Product_ID: str
    Product_Name: str
    Category: str
    Inventory_Level: int
    Quantity_Sold: int
    Price: float
    Sales_Value: float
    Cash_Received: float
    Expiration_Date: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "Date": "2025-08-25T00:00:00",
                "Product_ID": "PROD001",
                "Product_Name": "Product A",
                "Category": "OTC",
                "Inventory_Level": 100,
                "Quantity_Sold": 10,
                "Price": 15.50,
                "Sales_Value": 155.00,
                "Cash_Received": 155.00,
                "Expiration_Date": "2026-08-25T00:00:00"
            }
        }

class KPIDataInDB(KPIData):
    id: PyObjectId = Field(alias="_id")

class DailyKPI(BaseModel):
    date: datetime
    total_stockouts: int
    total_near_expiries: int
    top_sellers: List[dict]
    total_rx_volume: int
    total_sales_value: float
    total_cash_reconciliation: float
    inventory_levels_top_sellers: List[dict]
    branch_id: Optional[int] = None
    description: str

class DailyKPIInDB(DailyKPI):
    id: PyObjectId = Field(alias="_id")

class NearExpiry(BaseModel):
    date: datetime
    product_id: str
    product_name: str
    expiration_date: datetime
    days_to_expiry: int
    description: str
