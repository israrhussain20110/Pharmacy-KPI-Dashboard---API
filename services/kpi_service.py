'''
This service handles the business logic for fetching and analyzing KPI data.
'''
from database import get_database
from models import DailyKPIInDB
from datetime import datetime, timedelta

class KPIService:
    async def get_daily_kpis(self, branch_id: int = None):
        db = await get_database()
        query = {}
        if branch_id:
            query["branch_id"] = branch_id
        kpis = await db["daily_kpis"].find(query).to_list(1000)
        return [DailyKPIInDB(**kpi) for kpi in kpis]

    async def get_kpi_trends(self, branch_id: int = None):
        # This is a placeholder for a more complex trend analysis.
        # For now, we'll just return the last 7 days of data.
        db = await get_database()
        query = {"date": {"$gte": datetime.now() - timedelta(days=7)}}
        if branch_id:
            query["branch_id"] = branch_id
        kpis = await db["daily_kpis"].find(query).to_list(1000)
        return [DailyKPIInDB(**kpi) for kpi in kpis]

    async def get_kpi_alerts(self, branch_id: int = None):
        db = await get_database()
        query = {"total_stockouts": {"$gt": 0}}
        if branch_id:
            query["branch_id"] = branch_id
        alerts = await db["daily_kpis"].find(query).to_list(1000)
        return [DailyKPIInDB(**alert) for alert in alerts]

kpi_service = KPIService()
