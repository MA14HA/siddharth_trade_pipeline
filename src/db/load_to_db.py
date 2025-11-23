# src/db/load_to_db.py

import pandas as pd
from sqlalchemy import create_engine
import re

# ----------------------------------------------------------------------
# !!! CRITICAL: UPDATE THESE CREDENTIALS FOR YOUR POSTGRESQL SETUP !!!
# ----------------------------------------------------------------------
DB_USER = "postgres"  # Your PostgreSQL username
DB_PASSWORD = "1234" # <<< MUST BE YOUR ACTUAL POSTGRES PASSWORD
DB_HOST = "localhost"
DB_PORT = "5432"      # Default port
DB_NAME = "trade_analysis"
# ----------------------------------------------------------------------

def standardize_df_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes all DataFrame column names to lowercase snake_case
    (e.g., 'PORT CODE' -> 'port_code') to prevent case/space issues 
    during PostgreSQL loading.
    """
    cols = df.columns
    # 1. Replace spaces, hyphens, and dots with underscore
    cols = cols.str.replace(r'[\s\.\-]+', '_', regex=True)
    # 2. Convert to lowercase
    cols = cols.str.lower()
    
    df.columns = cols
    return df


def load_data_to_postgres(csv_path: str, table_name: str = 'shipments'):
    """
    Loads the cleaned CSV data into the PostgreSQL database.
    
    Uses if_exists="replace" to force a clean table creation, matching the 
    standardized DataFrame schema exactly.
    """
    try:
        # 1. Load the processed CSV
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} rows from CSV: {csv_path}")

        # 2. STANDARDIZE COLUMNS TO SNAKE_CASE (CRITICAL FIX)
        df = standardize_df_columns(df)
        print("DataFrame columns standardized to snake_case.")

        # 3. Create the SQLAlchemy Engine
        conn_string = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        engine = create_engine(conn_string)
        
        # 4. Write DataFrame to PostgreSQL
        # if_exists="replace" drops the old table and creates a new one 
        # based on the DataFrame's current schema. This fixes the schema conflict error.
        df.to_sql(
            table_name, 
            engine, 
            if_exists="replace", # <<< THE FINAL FIX >>>
            index=False,
            chunksize=1000
        )
        print(f"Successfully loaded data into PostgreSQL table '{table_name}'.")
        
    except Exception as e:
        print(f"An error occurred during PostgreSQL loading.")
        print(f"Error details: {e}")
        print("\nACTION REQUIRED: Check your DB credentials, and ensure the PostgreSQL service is running.")