-- Dates are m/d/Y; the source mixes zero-padded and unpadded fields
-- ("02/28/2005" and "2/28/2005"), which %m/%d/%Y parses either way.
SELECT
    "Storm_ID"                              AS storm_id,
    "Region"                                AS region,
    CAST("Region_Code" AS INTEGER)          AS region_code,
    strptime("Start", '%m/%d/%Y')::DATE     AS start_date,
    strptime("End", '%m/%d/%Y')::DATE       AS end_date,
    CAST("Year" AS INTEGER)                 AS year,
    CAST("Month" AS INTEGER)                AS month,
    CAST("RSI" AS DOUBLE)                   AS rsi,
    CAST("Category" AS INTEGER)             AS category,
    CAST("Term1Pct" AS DOUBLE)              AS term1_pct,
    CAST("Term2Pct" AS DOUBLE)              AS term2_pct,
    CAST("Term3Pct" AS DOUBLE)              AS term3_pct,
    CAST("Term4Pct" AS DOUBLE)              AS term4_pct,
    CAST("Area0" AS BIGINT)                 AS area0,
    CAST("Area1" AS BIGINT)                 AS area1,
    CAST("Area2" AS BIGINT)                 AS area2,
    CAST("Area3" AS BIGINT)                 AS area3,
    CAST("Area4" AS BIGINT)                 AS area4,
    CAST("Pop0" AS BIGINT)                  AS pop0,
    CAST("Pop1" AS BIGINT)                  AS pop1,
    CAST("Pop2" AS BIGINT)                  AS pop2,
    CAST("Pop3" AS BIGINT)                  AS pop3,
    CAST("Pop4" AS BIGINT)                  AS pop4
FROM "noaa-regional-snowfall-index"
