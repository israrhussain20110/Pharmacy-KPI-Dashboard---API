import pandas as pd
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from services.data_preprocessing import preprocess_kpi_data, convert_df_to_docs

async def load_csv_to_mongodb(csv_file_path: str):
    """
    Loads data from a CSV file, preprocesses it, and inserts it into MongoDB.
    """
    client = None
    try:
        print(f"Connecting to MongoDB at {settings.DATABASE_URL}...")
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        db = client[settings.DATABASE_NAME]
        collection = db[settings.COLLECTION_NAME]

        print(f"Reading CSV from {csv_file_path}...")
        df = pd.read_csv(csv_file_path)

        print("Preprocessing data...")
        processed_df = preprocess_kpi_data(df)
        docs = convert_df_to_docs(processed_df)

        if docs:
            print(f"Inserting {len(docs)} documents into collection '{settings.COLLECTION_NAME}'...")
            # Optional: Clear existing data before inserting
            # await collection.delete_many({})
            result = await collection.insert_many(docs)
            print(f"Successfully inserted {len(result.inserted_ids)} documents.")
        else:
            print("No documents to insert.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    # This path is relative to the project root when running from there
    # If running this script directly, adjust the path as needed.
    csv_path = "data/all_in_one_kpi_dataset.csv"
    asyncio.run(load_csv_to_mongodb(csv_path))
