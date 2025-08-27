from database import db_client
from config import settings

async def get_db_collection():
    return db_client.db[settings.COLLECTION_NAME]

async def get_db_client():
    return db_client.client
