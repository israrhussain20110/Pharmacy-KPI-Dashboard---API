
'''
This script calculates daily KPIs from the all_in_one_kpi_dataset.csv file.
'''
import pandas as pd
from datetime import datetime, timedelta

def calculate_daily_kpis(file_path, report_path):
    '''
    Calculates and prints daily KPIs from the given CSV file.

    Args:
        file_path (str): The path to the CSV file.
        report_path (str): The path to save the report.
    '''
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return

    df['Date'] = pd.to_datetime(df['Date'])
    df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])

    with open(report_path, 'w') as f:
        for date in sorted(df['Date'].unique()):
            daily_data = df[df['Date'] == date]
            f.write(f"--- Daily KPIs for {pd.to_datetime(date).strftime('%Y-%m-%d')} ---\n")

            # Stockouts
            stockouts = daily_data[daily_data['Inventory_Level'] == 0]
            f.write(f"Stockouts: {len(stockouts)} products\n")

            # Near-expiries
            near_expiry_date = date + timedelta(days=30)
            near_expiries = daily_data[daily_data['Expiration_Date'] <= near_expiry_date]
            f.write(f"Near Expiries (within 30 days): {len(near_expiries)} products\n")

            # Top sellers
            top_sellers = daily_data.sort_values(by='Quantity_Sold', ascending=False).head(3)
            f.write("Top 3 Sellers:\n")
            for _, row in top_sellers.iterrows():
                f.write(f"  - {row['Product_Name']}: {row['Quantity_Sold']} units\n")

            # Rx volume
            rx_volume = daily_data[daily_data['Category'] == 'Rx']['Quantity_Sold'].sum()
            f.write(f"Rx Volume: {rx_volume} units\n")

            # Sales value
            total_sales = daily_data['Sales_Value'].sum()
            f.write(f"Total Sales Value: ${total_sales:.2f}\n")

            # Cash reconciliation
            cash_reconciliation = daily_data['Cash_Received'].sum() - total_sales
            f.write(f"Cash Reconciliation: ${cash_reconciliation:.2f}\n")

            # Key inventory levels
            f.write("Inventory Levels for Top Sellers:\n")
            for _, row in top_sellers.iterrows():
                f.write(f"  - {row['Product_Name']}: {row['Inventory_Level']} units\n")

            f.write("\n\n")

if __name__ == "__main__":
    calculate_daily_kpis(
        'c:\\Users\\Ahmed\\DEV PROJECTS\\pharmacy-kpi\\data\\all_in_one_kpi_dataset.csv',
        'c:\\Users\\Ahmed\\DEV PROJECTS\\pharmacy-kpi\\reporting\\daily_kpi_report.txt'
    )

