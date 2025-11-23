-- sql/supplier_analysis.sql
-- Determines the activity status for suppliers (assuming IEC is the unique supplier ID).

WITH supplier_activity AS (
    -- 1. Get the min/max activity year for each unique supplier (IEC)
    SELECT
        iec,
        MIN(year) AS first_year,
        MAX(year) AS last_year
    FROM shipments
    WHERE iec IS NOT NULL
    GROUP BY iec
)
SELECT
    iec AS supplier_id,
    first_year,
    last_year,
    CASE
        -- Active: Had shipment in the target year (2025)
        WHEN last_year = 2025 THEN 'Active in 2025'
        
        -- Churned: Had shipments before 2025, but none in 2025 (i.e., last activity < 2025)
        WHEN last_year < 2025 THEN 'Churned'
        
        -- Historical: Catch-all for those active in the data range but not defined as Active/Churned 
        -- (e.g., if data only went up to 2024, they'd be historical, though this logic favors Churned)
        ELSE 'Historical' 
    END AS supplier_status

FROM supplier_activity
ORDER BY supplier_status, last_year DESC;