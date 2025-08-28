'''
This router handles the API endpoints for KPIs.
'''
from fastapi import APIRouter, Depends, Query
from services.kpi_service import kpi_service, KPIService
from models import DailyKPIInDB
from typing import List, Optional
from datetime import date

router = APIRouter(
    prefix="/kpis",
    tags=["kpis"],
)

@router.get("/daily", response_model=List[DailyKPIInDB])
async def get_daily_kpis(
    service: KPIService = Depends(lambda: kpi_service),
    start_date: Optional[date] = Query(None, description="Start date for KPI data (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for KPI data (YYYY-MM-DD)"),
    branch_id: Optional[int] = Query(None, description="Branch ID for KPI data"),
):
    return await service.get_daily_kpis(branch_id=branch_id, start_date=start_date, end_date=end_date)

@router.get("/trends", response_model=List[DailyKPIInDB])
async def get_kpi_trends(service: KPIService = Depends(lambda: kpi_service)):
    return await service.get_kpi_trends()

@router.get("/trends/{branch_id}", response_model=List[DailyKPIInDB])
async def get_kpi_trends_by_branch(branch_id: int, service: KPIService = Depends(lambda: kpi_service)):
    return await service.get_kpi_trends(branch_id)

@router.get("/alerts", response_model=List[DailyKPIInDB])
async def get_kpi_alerts(service: KPIService = Depends(lambda: kpi_service)):
    return await service.get_kpi_alerts()

@router.get("/alerts/{branch_id}", response_model=List[DailyKPIInDB])
async def get_kpi_alerts_by_branch(branch_id: int, service: KPIService = Depends(lambda: kpi_service)):
    return await service.get_kpi_alerts(branch_id)
