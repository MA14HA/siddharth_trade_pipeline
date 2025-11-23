import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Grand Total, Landed Cost Per Unit, and Category/Sub-Category.
    """
    
    # Use the correct, clean column names
    TOTAL_VALUE_COL = 'TOTAL VALUE_INR'
    DUTY_PAID_COL = 'DUTY PAID_INR'
    QUANTITY_COL = 'QUANTITY'
    DESCRIPTION_COL = 'GOODS DESCRIPTION'
    
    # 1. Compute Grand Total
    df["grand_total_inr"] = df[TOTAL_VALUE_COL] + df[DUTY_PAID_COL]
    
    # 2. Calculate Landed Cost Per Unit (Avoid division by zero)
    # Note: QUANTITY was filled with 0 in clean_base.py
    df["landed_cost_per_unit"] = np.where(
        df[QUANTITY_COL] > 0,
        df["grand_total_inr"] / df[QUANTITY_COL],
        None # Use None or NaN if quantity is zero
    )
    
    # 3. Category & Sub-Category Assignment
    
    # Assign Category
    def assign_category(desc):
        if not isinstance(desc, str): return "Others"
        desc_upper = desc.upper()
        if "GLASS" in desc_upper: return "Glassware"
        if "WOOD" in desc_upper or "WOODEN" in desc_upper: return "Woodenware"
        if "STEEL" in desc_upper or "SS" in desc_upper: return "Metalware"
        if "CERAMIC" in desc_upper: return "Ceramics"
        return "Others"

    df["category"] = df[DESCRIPTION_COL].apply(assign_category)

    # Assign Sub-Category
    def assign_subcategory(row):
        desc = row[DESCRIPTION_COL].upper()
        cat = row["category"]
        
        if cat == "Glassware":
            if "BOROSILICATE" in desc: return "Borosilicate"
            if "OPAL" in desc or "OPALWARE" in desc: return "Opalware"
        
        if cat == "Woodenware":
            if "SPOON" in desc: return "Spoon/Cutlery"
            if "FORK" in desc: return "Fork/Cutlery"
        
        return "General " + cat
    
    df["sub_category"] = df.apply(assign_subcategory, axis=1)

    return df