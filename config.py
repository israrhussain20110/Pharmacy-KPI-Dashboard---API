import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Pharmacy KPI Project"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DATABASE_NAME: str = os.getenv("MONGO_DB_NAME", "pharmacy_kpi_db")
    COLLECTION_NAME: str = os.getenv("MONGO_COLLECTION_NAME", "kpi_data")

settings = Settings()
