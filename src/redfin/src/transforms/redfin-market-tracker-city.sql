WITH sel AS (
    SELECT
        CAST(PERIOD_BEGIN AS DATE) AS date,
        TRIM(REGION) AS region_name,
    NULLIF(TRIM(STATE_CODE), '') AS state_code,
        TRY_CAST(MEDIAN_SALE_PRICE AS DOUBLE) AS median_sale_price,
    TRY_CAST(MEDIAN_LIST_PRICE AS DOUBLE) AS median_list_price,
    TRY_CAST(MEDIAN_PPSF AS DOUBLE) AS median_price_per_sqft,
    TRY_CAST(MEDIAN_LIST_PPSF AS DOUBLE) AS median_list_price_per_sqft,
    TRY_CAST(HOMES_SOLD AS DOUBLE) AS homes_sold,
    TRY_CAST(PENDING_SALES AS DOUBLE) AS pending_sales,
    TRY_CAST(NEW_LISTINGS AS DOUBLE) AS new_listings,
    TRY_CAST(INVENTORY AS DOUBLE) AS inventory,
    TRY_CAST(MONTHS_OF_SUPPLY AS DOUBLE) AS months_of_supply,
    TRY_CAST(MEDIAN_DOM AS DOUBLE) AS median_days_on_market,
    TRY_CAST(AVG_SALE_TO_LIST AS DOUBLE) AS avg_sale_to_list_ratio,
    TRY_CAST(SOLD_ABOVE_LIST AS DOUBLE) AS pct_sold_above_list,
    TRY_CAST(PRICE_DROPS AS DOUBLE) AS pct_price_drops,
    TRY_CAST(OFF_MARKET_IN_TWO_WEEKS AS DOUBLE) AS pct_off_market_two_weeks
    FROM "redfin-market-tracker-city"
    WHERE TRIM(PROPERTY_TYPE) = 'All Residential'
      AND lower(IS_SEASONALLY_ADJUSTED) IN ('false', 'f', '0')
)
SELECT * FROM sel
WHERE coalesce(median_sale_price, median_list_price, median_price_per_sqft, median_list_price_per_sqft, homes_sold, pending_sales, new_listings, inventory, months_of_supply, median_days_on_market, avg_sale_to_list_ratio, pct_sold_above_list, pct_price_drops, pct_off_market_two_weeks) IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY date, region_name ORDER BY region_name) = 1
