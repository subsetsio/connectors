SELECT
    strptime(CAST(month_date_yyyymm AS VARCHAR), '%Y%m')::DATE AS date,
    lpad(CAST(county_fips AS VARCHAR), 5, '0') AS county_fips, county_name, CAST(cbsa_code AS VARCHAR) AS cbsa_code, cbsa_title AS metro_name,

CAST(hotness_rank AS BIGINT)            AS hotness_rank,
CAST(hotness_score AS DOUBLE)           AS hotness_score,
CAST(supply_score AS DOUBLE)            AS supply_score,
CAST(demand_score AS DOUBLE)            AS demand_score,
CAST(median_days_on_market AS BIGINT)   AS median_days_on_market,
CAST(median_listing_price AS DOUBLE)    AS median_listing_price

FROM "realtor-hotness-county"
WHERE county_fips IS NOT NULL
