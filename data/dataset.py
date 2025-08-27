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

# Number of branches
num_branches = 3 # Let's start with 3 branches for simulation

data = []
for branch_id in range(1, num_branches + 1):
    for date in dates:
        for pid, pname, cat in zip(product_ids, products, categories):
            # Introduce some variation based on branch_id
            if branch_id == 1: # Urban branch - higher Rx volume
                qty_sold = np.random.poisson(15) if cat == 'Rx' else np.random.poisson(10)
                price = np.random.uniform(7, 60)
            elif branch_id == 2: # Rural branch - higher OTC sales
                qty_sold = np.random.poisson(8) if cat == 'Rx' else np.random.poisson(25)
                price = np.random.uniform(4, 40)
            else: # Average branch
                qty_sold = np.random.poisson(10) if cat == 'Rx' else np.random.poisson(20)
                price = np.random.uniform(5, 50)

            sales_value = qty_sold * price
            inventory_level = np.random.randint(0, 100)
            exp_date = date + timedelta(days=np.random.randint(1, 365))
            cash_received = sales_value + np.random.normal(0, 5)  # Small discrepancy
            
            data.append({
                'Branch_ID': branch_id,
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