
'''
This script loads calculated daily KPIs into the MongoDB database.
'''
import pandas as pd
from datetime import datetime, timedelta
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from models import DailyKPI

async def load_kpis_to_db():
    '''
    Calculates and loads daily KPIs into the MongoDB database.
    '''
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = client[settings.DATABASE_NAME]
    kpi_collection = db["daily_kpis"]
    await kpi_collection.delete_many({})

    try:
        df = pd.read_csv(r'c:\Users\Ahmed\DEV PROJECTS\pharmacy-kpi\data\all_in_one_kpi_dataset.csv')
    except FileNotFoundError:
        print("Error: The CSV file was not found.")
        return

    df['Date'] = pd.to_datetime(df['Date'])
    df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])

    for branch_id in df['branch_id'].unique():
        branch_data = df[df['branch_id'] == branch_id]
        for date in sorted(branch_data['Date'].unique()):
            daily_data = branch_data[branch_data['Date'] == date]

            stockouts = daily_data[daily_data['Inventory_Level'] == 0]
            near_expiry_date = date + timedelta(days=30)
            near_expiries = daily_data[daily_data['Expiration_Date'] <= near_expiry_date]
            top_sellers = daily_data.sort_values(by='Quantity_Sold', ascending=False).head(3)
            rx_volume = daily_data[daily_data['Category'] == 'Rx']['Quantity_Sold'].sum()
            total_sales = daily_data['Sales_Value'].sum()
            cash_reconciliation = daily_data['Cash_Received'].sum() - total_sales

            description = (
                f"Daily KPI report for {date.strftime('%Y-%m-%d')}. "
                f"Total sales: ${total_sales:.2f}, Rx volume: {int(rx_volume)} units, "
                f"Stockouts: {len(stockouts)} products, Near expiries: {len(near_expiries)} products."
            )

            kpi_data = DailyKPI(
                date=date,
                total_stockouts=len(stockouts),
                total_near_expiries=len(near_expiries),
                top_sellers=top_sellers[['Product_Name', 'Quantity_Sold']].to_dict('records'),
                total_rx_volume=int(rx_volume),
                total_sales_value=total_sales,
                total_cash_reconciliation=cash_reconciliation,
                inventory_levels_top_sellers=top_sellers[['Product_Name', 'Inventory_Level']].to_dict('records'),
                branch_id=int(branch_id),
                description=description
            )
            await kpi_collection.insert_one(kpi_data.dict())

    print("Successfully loaded daily KPIs into the database.")
    client.close()

if __name__ == "__main__":
    asyncio.run(load_kpis_to_db())
