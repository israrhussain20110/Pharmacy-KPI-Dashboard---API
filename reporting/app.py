from flask import Flask, render_template
import requests
import asyncio
import os

app = Flask(__name__, template_folder='templates')

FASTAPI_BASE_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

async def fetch_kpi_data_for_overview():
    kpi_data = {}
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/sales-value/")
        response.raise_for_status()
        kpi_data['sales_value'] = response.json()

        response = requests.get(f"{FASTAPI_BASE_URL}/cash-reconciliation/")
        response.raise_for_status()
        kpi_data['cash_reconciliation'] = response.json()

        response = requests.get(f"{FASTAPI_BASE_URL}/rx-volume/")
        response.raise_for_status()
        kpi_data['rx_volume'] = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching overview data from FastAPI: {e}")
        return {
            'sales_value': None,
            'cash_reconciliation': None,
            'rx_volume': None,
        }
    return kpi_data

async def fetch_kpi_data_for_inventory():
    kpi_data = {}
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/inventory-levels/")
        response.raise_for_status()
        kpi_data['inventory_levels'] = response.json()

        response = requests.get(f"{FASTAPI_BASE_URL}/stock-outs/")
        response.raise_for_status()
        kpi_data['stock_outs'] = response.json()

        response = requests.get(f"{FASTAPI_BASE_URL}/near-expiries/")
        response.raise_for_status()
        kpi_data['near_expiries'] = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching inventory data from FastAPI: {e}")
        return {
            'inventory_levels': [],
            'stock_outs': [],
            'near_expiries': [],
        }
    return kpi_data

async def fetch_kpi_data_for_products():
    kpi_data = {}
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/top-sellers/")
        response.raise_for_status()
        kpi_data['top_sellers'] = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data from FastAPI: {e}")
        return {
            'top_sellers': [],
        }
    return kpi_data

async def fetch_branch_comparison_data():
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/branches/compare")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching branch comparison data from FastAPI: {e}")
        return {}

@app.route('/')
async def overview_dashboard():
    data = await fetch_kpi_data_for_overview()
    return render_template('overview.html', **data)

@app.route('/inventory')
async def inventory_dashboard():
    data = await fetch_kpi_data_for_inventory()
    return render_template('inventory.html', **data)

@app.route('/products')
async def products_dashboard():
    data = await fetch_kpi_data_for_products()
    return render_template('products.html', **data)

@app.route('/branches')
async def branches_dashboard():
    data = await fetch_branch_comparison_data()
    return render_template('branches.html', **data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)