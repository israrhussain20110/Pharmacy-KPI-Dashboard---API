import pytest
from httpx import AsyncClient
from main import app
from database import db_client
from config import settings
import asyncio

# Use a test database for testing
settings.DATABASE_NAME = "pharmacy_kpi_test_db"
settings.COLLECTION_NAME = "kpi_test_data"

@pytest.fixture(scope="module")
async def test_client():
    # Connect to test database
    await db_client.connect()
    yield AsyncClient(app=app, base_url="http://test")
    # Clean up test database
    await db_client.db.drop_collection(settings.COLLECTION_NAME)
    await db_client.close()

@pytest.fixture(scope="module")
def event_loop():
    # Provide an event loop for pytest-asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_root_endpoint(test_client: AsyncClient):
    response = await test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Pharmacy KPI Project API!"}

@pytest.mark.asyncio
async def test_load_data_and_get_metrics(test_client: AsyncClient):
    # First, ensure the collection is empty
    await db_client.db[settings.COLLECTION_NAME].delete_many({})

    # Insert some dummy data for testing
    dummy_data = [
        {
            "date": "2025-08-25", "product_id": "P001", "product_name": "Product A", "category": "OTC",
            "initial_inventory": 100, "quantity_sold": 10, "price_per_unit": 10.0, "cash_received": 100.0,
            "expiration_date": "2026-08-25"
        },
        {
            "date": "2025-08-25", "product_id": "P002", "product_name": "Product B", "category": "Rx",
            "initial_inventory": 50, "quantity_sold": 5, "price_per_unit": 20.0, "cash_received": 100.0,
            "expiration_date": "2025-09-10" # Near expiry
        },
        {
            "date": "2025-08-25", "product_id": "P003", "product_name": "Product C", "category": "OTC",
            "initial_inventory": 0, "quantity_sold": 2, "price_per_unit": 5.0, "cash_received": 10.0,
            "expiration_date": "2026-01-01" # Stock out
        },
        {
            "date": "2025-08-26", "product_id": "P001", "product_name": "Product A", "category": "OTC",
            "initial_inventory": 90, "quantity_sold": 5, "price_per_unit": 10.0, "cash_received": 50.0,
            "expiration_date": "2026-08-25"
        }
    ]
    await db_client.db[settings.COLLECTION_NAME].insert_many(dummy_data)

    # Test total sales value
    response = await test_client.get("/sales-value/")
    assert response.status_code == 200
    assert response.json()["total_sales_value"] == 10*10 + 5*20 + 2*5 + 5*10 # 100 + 100 + 10 + 50 = 260

    # Test cash reconciliation
    response = await test_client.get("/cash-reconciliation/")
    assert response.status_code == 200
    assert response.json()["total_sales_value"] == 260
    assert response.json()["total_cash_received"] == 100 + 100 + 10 + 50 # 260
    assert response.json()["discrepancy"] == 0.0

    # Test Rx volume
    response = await test_client.get("/rx-volume/")
    assert response.status_code == 200
    assert response.json()["total_rx_volume"] == 5

    # Test top sellers
    response = await test_client.get("/top-sellers/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["product_id"] == "P001" # Product A: 10*10 + 5*10 = 150
    assert response.json()[1]["product_id"] == "P002" # Product B: 5*20 = 100
    assert response.json()[2]["product_id"] == "P003" # Product C: 2*5 = 10

    # Test near expiries
    response = await test_client.get("/near-expiries/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["product_id"] == "P002"

    # Test stock outs
    response = await test_client.get("/stock-outs/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["product_id"] == "P003"

    # Test inventory levels
    response = await test_client.get("/inventory-levels/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    # P001: initial 100, sold 10+5=15, current 100-15=85 (simplified, last record initial - total sold)
    # P002: initial 50, sold 5, current 50-5=45
    # P003: initial 0, sold 2, current 0-2=-2 (negative means more sold than initial)
    p001_level = next((item for item in response.json() if item["product_id"] == "P001"), None)
    assert p001_level["current_inventory"] == 90 - 5 # Based on the last record for P001
    p002_level = next((item for item in response.json() if item["product_id"] == "P002"), None)
    assert p002_level["current_inventory"] == 50 - 5
    p003_level = next((item for item in response.json() if item["product_id"] == "P003"), None)
    assert p003_level["current_inventory"] == 0 - 2
