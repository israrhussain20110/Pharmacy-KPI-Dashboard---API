from database import get_database
from config import settings

async def get_db_collection():
    db = await get_database()
    return db[settings.COLLECTION_NAME]
