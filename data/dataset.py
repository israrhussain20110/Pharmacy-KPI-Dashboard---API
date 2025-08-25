import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)  # For reproducibility

# Generate dates for 365 days starting from August 25, 2025
start_date = datetime(2025, 8, 25)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Product list (mix of Rx and OTC)
products = ['Aspirin', 'Insulin (Rx)', 'Bandages', 'Antibiotic (Rx)', 'Vitamins', 'Painkiller (Rx)', 'Shampoo', 'Cough Syrup (Rx)']
product_ids = range(1, 9)
categories = ['OTC', 'Rx', 'OTC', 'Rx', 'OTC', 'Rx', 'OTC', 'Rx']

data = []
for date in dates:
    for pid, pname, cat in zip(product_ids, products, categories):
        qty_sold = np.random.poisson(10) if cat == 'Rx' else np.random.poisson(20)
        price = np.random.uniform(5, 50)
        sales_value = qty_sold * price
        inventory_level = np.random.randint(0, 100)
        exp_date = date + timedelta(days=np.random.randint(1, 365))
        cash_received = sales_value + np.random.normal(0, 5)  # Small discrepancy
        
        data.append({
            'Date': date,
            'Product_ID': pid,
            'Product_Name': pname,
            'Category': cat,
            'Quantity_Sold': qty_sold,
            'Price': price,
            'Sales_Value': round(sales_value, 2),
            'Inventory_Level': inventory_level,
            'Expiration_Date': exp_date,
            'Cash_Received': round(cash_received, 2)
        })

df = pd.DataFrame(data)

# Save to CSV
df.to_csv('all_in_one_kpi_dataset.csv', index=False)

# Preview
print(df.head(10))