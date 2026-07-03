-- Zillow Home Value Index (ZHVI) by geography and month.
-- Pivots the long raw (one row per region/date/metric) to a wide table:
-- one row per (region_id, date), one typed column per metric.
SELECT
    CAST(date AS DATE) AS date,
    CAST(region_id AS BIGINT) AS region_id,
    ANY_VALUE(region_type) AS region_type,
    ANY_VALUE(region_name) AS region_name,
    ANY_VALUE(state_code) AS state_code,
    MAX(value) FILTER (WHERE metric = 'all_homes') AS all_homes,
    MAX(value) FILTER (WHERE metric = 'single_family') AS single_family,
    MAX(value) FILTER (WHERE metric = 'condo') AS condo,
    MAX(value) FILTER (WHERE metric = 'bed_1') AS bed_1,
    MAX(value) FILTER (WHERE metric = 'bed_2') AS bed_2,
    MAX(value) FILTER (WHERE metric = 'bed_3') AS bed_3,
    MAX(value) FILTER (WHERE metric = 'bed_4') AS bed_4,
    MAX(value) FILTER (WHERE metric = 'bed_5_plus') AS bed_5_plus,
    MAX(value) FILTER (WHERE metric = 'bottom_tier') AS bottom_tier,
    MAX(value) FILTER (WHERE metric = 'top_tier') AS top_tier
FROM "zillow-home-value"
GROUP BY region_id, date
