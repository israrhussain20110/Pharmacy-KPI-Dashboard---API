from datetime import date, timedelta
from typing import List, Dict, Any
from collections import defaultdict

def calculate_stock_outs(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculates stock-out events. A stock-out occurs if initial_inventory was 0 and quantity_sold was > 0.
    """
    stock_outs = []
    for record in data:
        if record.get('initial_inventory', 0) == 0 and record.get('quantity_sold', 0) > 0:
            stock_outs.append({
                "date": record.get('date'),
                "product_id": record.get('product_id'),
                "product_name": record.get('product_name'),
                "quantity_sold_during_stock_out": record.get('quantity_sold')
            })
    return stock_outs

def calculate_near_expiries(data: List[Dict[str, Any]], days_threshold: int = 30) -> List[Dict[str, Any]]:
    """
    Identifies products near expiry within a given threshold (default 30 days).
    Assumes 'expiration_date' is a string in ISO format or a datetime object.
    """
    near_expiries = []
    today = date.today()
    for record in data:
        exp_date_str = record.get('expiration_date')
        if exp_date_str:
            if isinstance(exp_date_str, str):
                exp_date = date.fromisoformat(exp_date_str.split('T')[0]) # Handle potential time part
            elif isinstance(exp_date_str, date):
                exp_date = exp_date_str
            else:
                continue # Skip if not string or date

            if exp_date - today <= timedelta(days=days_threshold) and exp_date >= today:
                near_expiries.append({
                    "date": record.get('date'),
                    "product_id": record.get('product_id'),
                    "product_name": record.get('product_name'),
                    "expiration_date": record.get('expiration_date'),
                    "days_to_expiry": (exp_date - today).days
                })
    return near_expiries

def calculate_top_sellers(data: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Identifies top selling products by total sales value.
    """
    product_sales = defaultdict(float)
    for record in data:
        product_id = record.get('product_id')
        sales_value = record.get('quantity_sold', 0) * record.get('price_per_unit', 0)
        if product_id:
            product_sales[product_id] += sales_value

    sorted_products = sorted(product_sales.items(), key=lambda item: item[1], reverse=True)
    top_sellers = []
    for prod_id, total_sales in sorted_products[:top_n]:
        # Find product name for the top seller
        product_name = next((item['product_name'] for item in data if item['product_id'] == prod_id), "Unknown")
        top_sellers.append({
            "product_id": prod_id,
            "product_name": product_name,
            "total_sales_value": total_sales
        })
    return top_sellers

def calculate_rx_volume(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates total prescription (Rx) volume.
    """
    total_rx_volume = 0
    for record in data:
        if record.get('category') == 'Rx':
            total_rx_volume += record.get('quantity_sold', 0)
    return {"total_rx_volume": total_rx_volume}

def calculate_total_sales_value(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates the total sales value.
    """
    total_sales = sum(record.get('quantity_sold', 0) * record.get('price_per_unit', 0) for record in data)
    return {"total_sales_value": total_sales}

def calculate_cash_reconciliation(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compares total sales value with total cash received.
    """
    total_sales = sum(record.get('quantity_sold', 0) * record.get('price_per_unit', 0) for record in data)
    total_cash_received = sum(record.get('cash_received', 0) for record in data)
    discrepancy = total_sales - total_cash_received
    return {
        "total_sales_value": total_sales,
        "total_cash_received": total_cash_received,
        "discrepancy": discrepancy
    }

def calculate_inventory_levels(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculates end-of-day inventory levels for each product.
    NOTE: This is a simplified calculation.
    It aggregates total quantity sold per product across all provided records
    and subtracts it from the 'initial_inventory' of the LAST record encountered for that product.
    For a true, chronologically accurate end-of-day inventory across multiple days
    or varying initial inventory levels, a more robust approach is required.
    This would typically involve:
    1. Grouping data by product and date.
    2. Processing records chronologically for each product.
    3. Tracking inventory changes (initial_inventory + receipts - sales) day by day.
    """
    inventory_levels = defaultdict(lambda: {"initial_inventory": 0, "quantity_sold": 0, "current_inventory": 0})
    for record in data:
        product_id = record.get('product_id')
        if product_id:
            inventory_levels[product_id]["product_name"] = record.get('product_name')
            # Update initial_inventory to the last seen for this product
            inventory_levels[product_id]["initial_inventory"] = record.get('initial_inventory', 0)
            inventory_levels[product_id]["quantity_sold"] += record.get('quantity_sold', 0)
            # Current inventory based on the last initial_inventory and aggregated sales
            inventory_levels[product_id]["current_inventory"] = inventory_levels[product_id]["initial_inventory"] - inventory_levels[product_id]["quantity_sold"]

    result = []
    for prod_id, details in inventory_levels.items():
        result.append({
            "product_id": prod_id,
            "product_name": details["product_name"],
            "initial_inventory": details["initial_inventory"],
            "quantity_sold_total": details["quantity_sold"],
            "current_inventory": details["current_inventory"]
        })
    return result
