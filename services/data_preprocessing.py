import pandas as pd
from datetime import datetime

def preprocess_kpi_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the raw KPI data DataFrame.
    - Converts 'date' and 'expiration_date' columns to datetime objects.
    - Ensures numerical columns are of the correct type.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])

    # Ensure numerical columns are correct types
    numerical_cols = ['Quantity_Sold', 'Price', 'Cash_Received', 'branch_id']
    for col in numerical_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # Coerce errors to NaN, then fill NaN with 0

    return df

def convert_df_to_docs(df: pd.DataFrame) -> list[dict]:
    """
    Converts a pandas DataFrame to a list of dictionaries, suitable for MongoDB insertion.
    Ensures date fields are in ISO format.
    """
    records = df.to_dict(orient='records')
    for record in records:
        if isinstance(record.get('Date'), pd.Timestamp):
            record['Date'] = record['Date'].isoformat()
        if isinstance(record.get('Expiration_Date'), pd.Timestamp):
            record['Expiration_Date'] = record['Expiration_Date'].isoformat()
    return records
