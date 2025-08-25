from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class KPIData(BaseModel):
    date: date
    product_id: str
    product_name: str
    category: str
    initial_inventory: int
    quantity_sold: int
    price_per_unit: float
    cash_received: float
    expiration_date: date

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2025-08-25",
                "product_id": "PROD001",
                "product_name": "Product A",
                "category": "OTC",
                "initial_inventory": 100,
                "quantity_sold": 10,
                "price_per_unit": 15.50,
                "cash_received": 155.00,
                "expiration_date": "2026-08-25"
            }
        }

class KPIDataInDB(KPIData):
    id: str = Field(alias="_id")
