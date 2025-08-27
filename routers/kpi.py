'''
This router handles the API endpoints for KPIs.
'''
from fastapi import APIRouter, Depends
from services.kpi_service import kpi_service, KPIService
from models import DailyKPIInDB
from typing import List

router = APIRouter(
    prefix="/kpis",
    tags=["kpis"],
)

@router.get("/daily", response_model=List[DailyKPIInDB])
async def get_daily_kpis(service: KPIService = Depends(lambda: kpi_service)):
    return await service.get_daily_kpis()

@router.get("/daily/{branch_id}", response_model=List[DailyKPIInDB])
async def get_daily_kpis_by_branch(branch_id: int, service: KPIService = Depends(lambda: kpi_service)):
    return await service.get_daily_kpis(branch_id)

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
