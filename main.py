from fastapi import FastAPI
from database import db_client
from config import settings
from routers import (
    stock_outs,
    near_expiries,
    top_sellers,
    rx_volume,
    sales_value,
    cash_reconciliation,
    inventory_levels,
    branch_comparison,
    transfers, # New import
    kpi
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

@app.on_event("startup")
async def startup_db_client():
    await db_client.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db_client.close()

app.include_router(stock_outs.router)
app.include_router(near_expiries.router)
app.include_router(top_sellers.router)
app.include_router(rx_volume.router)
app.include_router(sales_value.router)
app.include_router(cash_reconciliation.router)
app.include_router(inventory_levels.router)
app.include_router(branch_comparison.router)
app.include_router(transfers.router) # New include
app.include_router(kpi.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Pharmacy KPI Project API!"}
