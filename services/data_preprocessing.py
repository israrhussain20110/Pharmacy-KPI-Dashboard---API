import pandas as pd
from datetime import datetime

def preprocess_kpi_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the raw KPI data DataFrame.
    - Converts 'date' and 'expiration_date' columns to datetime objects.
    - Ensures numerical columns are of the correct type.
    """
    df['date'] = pd.to_datetime(df['date'])
    df['expiration_date'] = pd.to_datetime(df['expiration_date'])

    # Ensure numerical columns are correct types
    numerical_cols = ['initial_inventory', 'quantity_sold', 'price_per_unit', 'cash_received']
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
        if isinstance(record.get('date'), pd.Timestamp):
            record['date'] = record['date'].isoformat()
        if isinstance(record.get('expiration_date'), pd.Timestamp):
            record['expiration_date'] = record['expiration_date'].isoformat()
    return records
