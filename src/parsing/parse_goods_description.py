import re
import pandas as pd

DESCRIPTION_COL = 'GOODS DESCRIPTION'

def extract_unit_price_usd(description: str) -> float | None:
    """
    Extracts the USD unit price from the description.
    Pattern: Looks for USD/$/@ followed by a number.
    e.g., '@ USD 1.5/PC' or '$ 2.00 per unit'
    """
    if not isinstance(description, str):
        return None
    
    # Regex: Look for USD, $, or @, potentially followed by spaces, then capture the number (digits and a decimal point).
    pattern = r'(?:USD|\$|@)\s*([\d\.]+)'
    match = re.search(pattern, description.upper())
    
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None

def extract_capacity_spec(description: str) -> str | None:
    """
    Extracts capacity or size specifications.
    Pattern: Looks for a number followed by common unit abbreviations.
    e.g., '500ML', '1.5 LTR', '10 INCH'
    """
    if not isinstance(description, str):
        return None
    
    # Regex: (Number with optional decimal) + (space) + (Unit like ML, LTR, INCH, CM, MM, KG, KGS, TON)
    pattern = r'(\d+\.?\d*)\s*(ML|LTR|L|INCH|CM|MM|KG|KGS|TON|MT)(?:S|\b)'
    match = re.search(pattern, description.upper())
    
    if match:
        # Returns the number and the unit (e.g., '500 ML')
        return f"{match.group(1)} {match.group(2).upper()}"
    return None

def extract_material_type(description: str) -> str | None:
    """
    Extracts common material types based on keywords.
    """
    if not isinstance(description, str):
        return None
    
    description_upper = description.upper()
    if 'BOROSILICATE' in description_upper: return 'Borosilicate Glass'
    if 'OPALWARE' in description_upper or 'OPAL' in description_upper: return 'Opalware'
    if 'WOODEN' in description_upper or 'WOOD' in description_upper: return 'Wood'
    if 'STEEL' in description_upper or 'SS' in description_upper: return 'Stainless Steel'
    if 'CERAMIC' in description_upper: return 'Ceramic'
    
    return None

def parse_goods_description(df: pd.DataFrame) -> pd.DataFrame:
    """Applies all parsing functions to the GOODS DESCRIPTION column."""
    
    df["unit_price_in_usd"] = df[DESCRIPTION_COL].apply(extract_unit_price_usd)
    df["capacity_spec"] = df[DESCRIPTION_COL].apply(extract_capacity_spec)
    df["material_type"] = df[DESCRIPTION_COL].apply(extract_material_type)
    
    # Model name/number is highly dependent on specific data; we'll leave it simple for now
    # Example placeholder: extracting the first word/token that looks like a model
    df["model_token"] = df[DESCRIPTION_COL].str.extract(r'([A-Z0-9]{2,}-\d{2,})', flags=re.IGNORECASE)
    
    return df