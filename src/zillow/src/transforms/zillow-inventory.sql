-- Zillow for-sale housing inventory flows (active listings, new listings, new pending) by geography and month.
-- Pivots the long raw (one row per region/date/metric) to a wide table:
-- one row per (region_id, date), one typed column per metric.
SELECT
    CAST(date AS DATE) AS date,
    CAST(region_id AS BIGINT) AS region_id,
    ANY_VALUE(region_type) AS region_type,
    ANY_VALUE(region_name) AS region_name,
    ANY_VALUE(state_code) AS state_code,
    MAX(value) FILTER (WHERE metric = 'for_sale_inventory') AS for_sale_inventory,
    MAX(value) FILTER (WHERE metric = 'new_listings') AS new_listings,
    MAX(value) FILTER (WHERE metric = 'new_pending') AS new_pending
FROM "zillow-inventory"
GROUP BY region_id, date
