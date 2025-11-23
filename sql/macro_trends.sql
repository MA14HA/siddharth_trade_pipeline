-- sql/macro_trends.sql (FIXED)
-- Calculates yearly totals and Year-over-Year (YoY) growth for core financial metrics.

WITH yearly_totals AS (
    SELECT
        year,
        SUM(total_value_inr) AS total_value_inr,
        SUM(duty_paid_inr) AS total_duty_paid_inr,
        SUM(grand_total_inr) AS total_grand_total
    FROM shipments
    GROUP BY year
    HAVING year IS NOT NULL
)
SELECT
    year,
    total_value_inr,
    total_duty_paid_inr,
    total_grand_total,
    
    -- FIXED: Explicitly cast the result to NUMERIC before rounding
    ROUND((100.0 * (total_value_inr - LAG(total_value_inr) OVER (ORDER BY year))
        / LAG(total_value_inr) OVER (ORDER BY year))::NUMERIC, 2) AS yoy_total_value_pct,
        
    -- FIXED: Explicitly cast the result to NUMERIC before rounding
    ROUND((100.0 * (total_grand_total - LAG(total_grand_total) OVER (ORDER BY year))
        / LAG(total_grand_total) OVER (ORDER BY year))::NUMERIC, 2) AS yoy_grand_total_pct
        
FROM yearly_totals
ORDER BY year;