-- Zillow sales and listing-price metrics by geography and month.
-- Pivots the long raw (one row per region/date/metric) to a wide table:
-- one row per (region_id, date), one typed column per metric.
SELECT
    CAST(date AS DATE) AS date,
    CAST(region_id AS BIGINT) AS region_id,
    ANY_VALUE(region_type) AS region_type,
    ANY_VALUE(region_name) AS region_name,
    ANY_VALUE(state_code) AS state_code,
    MAX(value) FILTER (WHERE metric = 'median_list_price') AS median_list_price,
    MAX(value) FILTER (WHERE metric = 'median_sale_price') AS median_sale_price,
    MAX(value) FILTER (WHERE metric = 'sales_count') AS sales_count,
    MAX(value) FILTER (WHERE metric = 'pct_sold_above_list') AS pct_sold_above_list,
    MAX(value) FILTER (WHERE metric = 'pct_sold_below_list') AS pct_sold_below_list,
    MAX(value) FILTER (WHERE metric = 'days_to_pending') AS days_to_pending,
    MAX(value) FILTER (WHERE metric = 'pct_price_cut') AS pct_price_cut
FROM "zillow-sales"
GROUP BY region_id, date
