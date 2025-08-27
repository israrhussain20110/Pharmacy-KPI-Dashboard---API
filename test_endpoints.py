import pytest
from starlette.testclient import TestClient
from main import app
from database import db_client
from config import settings
import asyncio

# Use a test database for testing
settings.DATABASE_NAME = "pharmacy_kpi_test_db"
settings.COLLECTION_NAME = "kpi_test_data"

@pytest.fixture(scope="module")
def test_client():
    # Connect to test database
    asyncio.run(db_client.connect())
    with TestClient(app) as client:
        yield client
    # Clean up test database
    asyncio.run(db_client.db.drop_collection(settings.COLLECTION_NAME))
    asyncio.run(db_client.close())

def test_root_endpoint(test_client: TestClient):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Pharmacy KPI Project API!"}

def test_load_data_and_get_metrics(test_client: TestClient):
    # First, ensure the collection is empty
    asyncio.run(db_client.db[settings.COLLECTION_NAME].delete_many({}))

    # Insert some dummy data for testing
    dummy_data = [
        {
            "Date": "2025-08-25", "Product_ID": "P001", "Product_Name": "Product A", "Category": "OTC",
            "Inventory_Level": 100, "Quantity_Sold": 10, "Price": 10.0, "Cash_Received": 100.0,
            "Expiration_Date": "2026-08-25", "branch_id": 1
        },
        {
            "Date": "2025-08-25", "Product_ID": "P002", "Product_Name": "Product B", "Category": "Rx",
            "Inventory_Level": 50, "Quantity_Sold": 5, "Price": 20.0, "Cash_Received": 100.0,
            "Expiration_Date": "2025-09-10", "branch_id": 1 # Near expiry
        },
        {
            "Date": "2025-08-25", "Product_ID": "P003", "Product_Name": "Product C", "Category": "OTC",
            "Inventory_Level": 0, "Quantity_Sold": 2, "Price": 5.0, "Cash_Received": 10.0,
            "Expiration_Date": "2026-01-01", "branch_id": 2 # Stock out
        },
        {
            "Date": "2025-08-26", "Product_ID": "P001", "Product_Name": "Product A", "Category": "OTC",
            "Inventory_Level": 90, "Quantity_Sold": 5, "Price": 10.0, "Cash_Received": 50.0,
            "Expiration_Date": "2026-08-25", "branch_id": 2
        }
    ]
    asyncio.run(db_client.db[settings.COLLECTION_NAME].insert_many(dummy_data))

    # Test total sales value
    response = test_client.get("/sales-value/")
    assert response.status_code == 200
    assert response.json()["total_sales_value"] == 10*10 + 5*20 + 2*5 + 5*10 # 100 + 100 + 10 + 50 = 260

    # Test total sales value for branch 1
    response = test_client.get("/sales-value/?branch_id=1")
    assert response.status_code == 200
    assert response.json()["total_sales_value"] == 10*10 + 5*20 # 100 + 100 = 200

    # Test cash reconciliation
    response = test_client.get("/cash-reconciliation/")
    assert response.status_code == 200
    assert response.json()["total_sales_value"] == 260
    assert response.json()["total_cash_received"] == 100 + 100 + 10 + 50 # 260
    assert response.json()["discrepancy"] == 0.0

    # Test Rx volume
    response = test_client.get("/rx-volume/")
    assert response.status_code == 200
    assert response.json()["total_rx_volume"] == 5

    # Test top sellers
    response = test_client.get("/top-sellers/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["product_id"] == "P001" # Product A: 10*10 + 5*10 = 150
    assert response.json()[1]["product_id"] == "P002" # Product B: 5*20 = 100
    assert response.json()[2]["product_id"] == "P003" # Product C: 2*5 = 10

    # Test near expiries for branch 1
    response = test_client.get("/near-expiries/?branch_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["product_id"] == "P002"

    # Test stock outs for branch 2
    response = test_client.get("/stock-outs/?branch_id=2")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["product_id"] == "P003"

    # Test inventory levels
    response = test_client.get("/inventory-levels/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    p001_level = next((item for item in response.json() if item["product_id"] == "P001"), None)
    assert p001_level["current_inventory"] == 90 - 15 # initial inventory is not used from the first record
    p002_level = next((item for item in response.json() if item["product_id"] == "P002"), None)
    assert p002_level["current_inventory"] == 50 - 5
    p003_level = next((item for item in response.json() if item["product_id"] == "P003"), None)
    assert p003_level["current_inventory"] == 0 - 2

def test_branch_comparison(test_client: TestClient):
    # First, ensure the collection is empty
    asyncio.run(db_client.db[settings.COLLECTION_NAME].delete_many({}))

    # Insert some dummy data for testing
    dummy_data = [
        {
            "Date": "2025-08-25", "Product_ID": "P001", "Product_Name": "Product A", "Category": "OTC",
            "Inventory_Level": 100, "Quantity_Sold": 10, "Price": 10.0, "Cash_Received": 100.0,
            "Expiration_Date": "2026-08-25", "branch_id": 1
        },
        {
            "Date": "2025-08-25", "Product_ID": "P002", "Product_Name": "Product B", "Category": "Rx",
            "Inventory_Level": 50, "Quantity_Sold": 5, "Price": 20.0, "Cash_Received": 100.0,
            "Expiration_Date": "2025-09-10", "branch_id": 1 # Near expiry
        },
        {
            "Date": "2025-08-25", "Product_ID": "P003", "Product_Name": "Product C", "Category": "OTC",
            "Inventory_Level": 0, "Quantity_Sold": 2, "Price": 5.0, "Cash_Received": 10.0,
            "Expiration_Date": "2026-01-01", "branch_id": 2 # Stock out
        },
        {
            "Date": "2025-08-26", "Product_ID": "P001", "Product_Name": "Product A", "Category": "OTC",
            "Inventory_Level": 90, "Quantity_Sold": 5, "Price": 10.0, "Cash_Received": 50.0,
            "Expiration_Date": "2026-08-25", "branch_id": 2
        }
    ]
    asyncio.run(db_client.db[settings.COLLECTION_NAME].insert_many(dummy_data))

    response = test_client.get("/branches/compare")
    assert response.status_code == 200
    data = response.json()
    assert "sales_by_branch" in data
    assert "inventory_turns_by_branch" in data
    assert "service_level_by_branch" in data
    assert data["sales_by_branch"]["1"] == 200
    assert data["sales_by_branch"]["2"] == 60
