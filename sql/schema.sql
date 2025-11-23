-- sql/schema.sql
-- Run this script in psql or pgAdmin connected to the trade_analysis database

-- 1. DROP the existing table to remove the old, mismatched schema
DROP TABLE IF EXISTS shipments;

-- 2. CREATE the new table with standardized column names
CREATE TABLE shipments (
    -------------------------------------------------------------------
    -- ORIGINAL DATA FIELDS (Standardized from Python)
    -------------------------------------------------------------------
    port_code VARCHAR(10),              -- from 'PORT CODE'
    date VARCHAR(20),                   -- from 'DATE'
    iec VARCHAR(30),
    hs_code VARCHAR(20),                -- from 'HS CODE'
    goods_description TEXT,             -- from 'GOODS DESCRIPTION'
    master_category VARCHAR(50),        -- from 'Master category'
    model_name VARCHAR(50),             -- from 'Model Name'
    model_number VARCHAR(50),           -- from 'Model Number'
    capacity VARCHAR(50),               -- from 'Capacity'
    qty NUMERIC(18, 2),                 -- from 'Qty'
    unit_of_measure VARCHAR(10),        -- from 'Unit of measure'
    price NUMERIC(10, 4),               -- from 'Price'
    unit_of_measure_1 VARCHAR(10),      -- from 'Unit of measure.1'
    
    -- Original Financials
    quantity NUMERIC(18, 2),            -- from 'QUANTITY' (Cleaned)
    unit VARCHAR(10),                   -- from 'UNIT'
    unit_price_inr NUMERIC(10, 4),      -- from 'UNIT PRICE_INR'
    total_value_inr NUMERIC(18, 2),     -- from 'TOTAL VALUE_INR'
    unit_price_in_usd NUMERIC(10, 4),  -- from 'UNIT PRICE_USD'
    total_value_usd NUMERIC(18, 2),     -- from 'TOTAL VALUE_USD'
    duty_paid_inr NUMERIC(18, 2),       -- from 'DUTY PAID_INR'
    
    -------------------------------------------------------------------
    -- CLEANED & ENGINEERED FIELDS (Created in Python Phases 2 & 3)
    -------------------------------------------------------------------
    date_of_shipment DATE,              -- Cleaned date object
    year INT,                           -- Derived year
    month INT,
    quarter INT,
    
    unit_standardized VARCHAR(10),      -- Standardized unit (PCS, KG)
    unit_price_usd NUMERIC(10, 4),      -- Parsed unit price
    capacity_spec VARCHAR(50),          -- Parsed capacity/size
    material_type VARCHAR(50),          -- Parsed material
    
    grand_total_inr NUMERIC(18, 2),     -- total_value + duty_paid
    landed_cost_per_unit NUMERIC(10, 4),-- cost / quantity
    category VARCHAR(50),               -- Derived category
    sub_category VARCHAR(50)            -- Derived sub-category
);