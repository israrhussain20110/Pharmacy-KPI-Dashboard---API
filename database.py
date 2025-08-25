from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.DATABASE_URL)
        self.db = self.client[settings.DATABASE_NAME]
        print(f"Connected to MongoDB: {settings.DATABASE_URL}, Database: {settings.DATABASE_NAME}")

    async def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

db_client = Database()

async def get_database():
    return db_client.db
