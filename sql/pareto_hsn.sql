-- sql/pareto_hsn.sql
-- Identifies Top HSN Codes and prepares data for cumulative analysis in BI tool.

WITH hsn_totals AS (
    -- 1. Calculate Total Value for each unique HS Code
    SELECT
        hs_code,
        SUM(total_value_inr) AS total_value_inr,
        -- Calculate the total value across ALL HSN codes using a window function
        SUM(SUM(total_value_inr)) OVER () AS overall_total
    FROM shipments
    GROUP BY hs_code
    HAVING hs_code IS NOT NULL
),
ranked_hsn AS (
    -- 2. Rank and calculate cumulative metrics
    SELECT
        hs_code,
        total_value_inr,
        -- Assign a rank number based on value (highest value = rank 1)
        ROW_NUMBER() OVER (ORDER BY total_value_inr DESC) AS rank_no,
        
        -- Calculate Individual Share (%): (Item Value / Overall Total) * 100
        -- Apply explicit cast (::NUMERIC) to allow ROUND() function
        ROUND((total_value_inr * 100.0 / overall_total)::NUMERIC, 2) AS share_of_total_pct,
        
        -- Calculate Cumulative Share (%): Running Total / Overall Total * 100
        ROUND((SUM(total_value_inr) OVER (ORDER BY total_value_inr DESC) * 100.0
          / overall_total)::NUMERIC, 2) AS cumulative_share_pct
          
    FROM hsn_totals
)
-- FINAL QUERY: Select all ranked items and use CASE to group the rest as 'OTHERS'.
SELECT
    rank_no,
    hs_code,
    total_value_inr,
    share_of_total_pct,
    cumulative_share_pct,
    -- Create the group label (Top 25 are labeled by their code, rest are 'OTHERS')
    -- We explicitly cast to VARCHAR(50) to prevent the BIGINT type conflict error.
    (CASE
        WHEN rank_no <= 25 THEN hs_code::VARCHAR(50)
        ELSE 'OTHERS'::VARCHAR(50)
    END) AS hsn_group
FROM ranked_hsn
ORDER BY rank_no;