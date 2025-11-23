# src/cleaning/clean_base.py

import pandas as pd
import numpy as np

def clean_base(df: pd.DataFrame) -> pd.DataFrame:
    DATE_COL = 'DATE'
    FINANCIAL_COLS = ['TOTAL VALUE_INR', 'DUTY PAID_INR', 'QUANTITY']
    
    # 1. Date Handling
    # VITAL CHANGE: Use 'infer_datetime_format=True' for better success rate
    df["date_of_shipment"] = pd.to_datetime(
        df[DATE_COL],
        errors="coerce",
        dayfirst=True,
        infer_datetime_format=True # Pandas will try harder to guess the format
    )

    # Derive Year, Month, Quarter
    df["year"] = df["date_of_shipment"].dt.year
    df["month"] = df["date_of_shipment"].dt.month
    df["quarter"] = df["date_of_shipment"].dt.quarter

    # Drop rows where date is critically missing (NaT)
    # We will only drop rows where the date is missing AND there is no other data
    df.dropna(subset=['date_of_shipment'], inplace=True) # Keep this line as per assignment
    
    # 2. Handle Basic Missing Data (Fixing the FutureWarning)
    for col in FINANCIAL_COLS:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # FIX: Explicit assignment to avoid inplace warning and copy error
        df[col] = df[col].fillna(0) 
    
    # 3. Final Quantity Check
    df['QUANTITY'] = np.where(df['QUANTITY'] < 0, 0, df['QUANTITY'].astype(int))

    return df