from datetime import date, timedelta, datetime
from typing import List, Dict, Any
from collections import defaultdict

def calculate_stock_outs(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculates stock-out events. A stock-out occurs if initial_inventory was 0 and quantity_sold was > 0.
    """
    stock_outs = []
    for record in data:
        if record.get('Inventory_Level', 0) == 0 and record.get('Quantity_Sold', 0) > 0:
            stock_outs.append({
                "date": record.get('Date'),
                "product_id": record.get('Product_ID'),
                "product_name": record.get('Product_Name'),
                "quantity_sold_during_stock_out": record.get('Quantity_Sold')
            })
    return stock_outs

def calculate_near_expiries(data: List[Dict[str, Any]], days_threshold: int = 30) -> List[Dict[str, Any]]:
    """
    Identifies products near expiry within a given threshold (default 30 days).
    Assumes 'Expiration_Date' is a string in ISO format or a datetime object.
    """
    near_expiries = []
    today = datetime.today()
    for record in data:
        exp_date_val = record.get('Expiration_Date')
        if exp_date_val:
            if isinstance(exp_date_val, str):
                exp_date = datetime.fromisoformat(exp_date_val.split('T')[0]) # Handle potential time part
            elif isinstance(exp_date_val, datetime):
                exp_date = exp_date_val
            else:
                continue # Skip if not string or datetime

            if exp_date - today <= timedelta(days=days_threshold) and exp_date >= today:
                near_expiries.append({
                    "date": record.get('Date'),
                    "product_id": record.get('Product_ID'),
                    "product_name": record.get('Product_Name'),
                    "expiration_date": record.get('Expiration_Date'),
                    "days_to_expiry": (exp_date - today).days
                })
    return near_expiries

def calculate_top_sellers(data: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Identifies top selling products by total sales value.
    """
    product_sales = defaultdict(float)
    for record in data:
        product_id = record.get('Product_ID')
        sales_value = record.get('Quantity_Sold', 0) * record.get('Price', 0)
        if product_id:
            product_sales[product_id] += sales_value

    sorted_products = sorted(product_sales.items(), key=lambda item: item[1], reverse=True)
    top_sellers = []
    for prod_id, total_sales in sorted_products[:top_n]:
        # Find product name for the top seller
        product_name = next((item['Product_Name'] for item in data if item['Product_ID'] == prod_id), "Unknown")
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
        if record.get('Category') == 'Rx':
            total_rx_volume += record.get('Quantity_Sold', 0)
    return {"total_rx_volume": total_rx_volume}

def calculate_total_sales_value(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates the total sales value.
    """
    total_sales = sum(record.get('Quantity_Sold', 0) * record.get('Price', 0) for record in data)
    return {"total_sales_value": total_sales}

def calculate_cash_reconciliation(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compares total sales value with total cash received.
    """
    total_sales = sum(record.get('Quantity_Sold', 0) * record.get('Price', 0) for record in data)
    total_cash_received = sum(record.get('Cash_Received', 0) for record in data)
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
    inventory_levels = defaultdict(lambda: {"Inventory_Level": 0, "Quantity_Sold": 0, "current_inventory": 0})
    for record in data:
        product_id = record.get('Product_ID')
        if product_id:
            inventory_levels[product_id]["product_name"] = record.get('Product_Name')
            # Update initial_inventory to the last seen for this product
            inventory_levels[product_id]["Inventory_Level"] = record.get('Inventory_Level', 0)
            inventory_levels[product_id]["Quantity_Sold"] += record.get('Quantity_Sold', 0)
            # Current inventory based on the last initial_inventory and aggregated sales
            inventory_levels[product_id]["current_inventory"] = inventory_levels[product_id]["Inventory_Level"] - inventory_levels[product_id]["Quantity_Sold"]

    result = []
    for prod_id, details in inventory_levels.items():
        result.append({
            "product_id": prod_id,
            "product_name": details["product_name"],
            "initial_inventory": details["Inventory_Level"],
            "quantity_sold_total": details["Quantity_Sold"],
            "current_inventory": details["current_inventory"]
        })
    return result
