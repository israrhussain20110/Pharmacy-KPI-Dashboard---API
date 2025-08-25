from pydantic import BaseModel, Field
from datetime import datetime # Use datetime for ISO format
from typing import Optional

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
    id: str = Field(alias="_id")
