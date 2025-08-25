from flask import Flask, render_template
import requests
import asyncio
import os # Import os to get environment variable

app = Flask(__name__, template_folder='templates')

# Base URL for the FastAPI backend - get from environment variable or use default
FASTAPI_BASE_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

async def fetch_kpi_data():
    """Fetches all necessary KPI data from the FastAPI backend."""
    kpi_data = {}
    try:
        # Fetch Total Sales Value
        response = requests.get(f"{FASTAPI_BASE_URL}/sales-value/")
        response.raise_for_status()
        kpi_data['sales_value'] = response.json()

        # Fetch Cash Reconciliation
        response = requests.get(f"{FASTAPI_BASE_URL}/cash-reconciliation/")
        response.raise_for_status()
        kpi_data['cash_reconciliation'] = response.json()

        # Fetch Rx Volume
        response = requests.get(f"{FASTAPI_BASE_URL}/rx-volume/")
        response.raise_for_status()
        kpi_data['rx_volume'] = response.json()

        # Fetch Top Sellers
        response = requests.get(f"{FASTAPI_BASE_URL}/top-sellers/")
        response.raise_for_status()
        kpi_data['top_sellers'] = response.json()

        # Fetch Near Expiries
        response = requests.get(f"{FASTAPI_BASE_URL}/near-expiries/")
        response.raise_for_status()
        kpi_data['near_expiries'] = response.json()

        # Fetch Stock-Out Events
        response = requests.get(f"{FASTAPI_BASE_URL}/stock-outs/")
        response.raise_for_status()
        kpi_data['stock_outs'] = response.json()

        # Fetch Inventory Levels
        response = requests.get(f"{FASTAPI_BASE_URL}/inventory-levels/")
        response.raise_for_status()
        kpi_data['inventory_levels'] = response.json()

    except requests.exceptions.ConnectionError:
        print(f"Could not connect to FastAPI backend at {FASTAPI_BASE_URL}. Is it running?")
        # Return empty data so the dashboard can still render
        return {
            'sales_value': None,
            'cash_reconciliation': None,
            'rx_volume': None,
            'top_sellers': [],
            'near_expiries': [],
            'stock_outs': [],
            'inventory_levels': []
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from FastAPI: {e}")
        return {
            'sales_value': None,
            'cash_reconciliation': None,
            'rx_volume': None,
            'top_sellers': [],
            'near_expiries': [],
            'stock_outs': [],
            'inventory_levels': []
        }
    return kpi_data

@app.route('/')
async def dashboard():
    data = await fetch_kpi_data()
    return render_template('dashboard.html', **data)

if __name__ == '__main__':
    # Run Flask app
    # Note: For production, use a production-ready WSGI server like Gunicorn
    app.run(debug=True, port=5000)
