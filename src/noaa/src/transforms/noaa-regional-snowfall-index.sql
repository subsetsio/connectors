SELECT
    REGION                          AS region,
    COALESCE(try_strptime("Start", '%m/%d/%Y')::DATE, TRY_CAST("Start" AS DATE)) AS start_date,
    COALESCE(try_strptime("End", '%m/%d/%Y')::DATE, TRY_CAST("End" AS DATE))     AS end_date,
    TRY_CAST(RSI AS DOUBLE)         AS rsi,
    TRY_CAST(CATEGORY AS INT)       AS category,
    TRY_CAST(TERM1PCT AS DOUBLE)    AS term1_pct,
    TRY_CAST(TERM2PCT AS DOUBLE)    AS term2_pct,
    TRY_CAST(TERM3PCT AS DOUBLE)    AS term3_pct,
    TRY_CAST(TERM4PCT AS DOUBLE)    AS term4_pct,
    TRY_CAST(AREA0 AS BIGINT)       AS area0,
    TRY_CAST(POP0 AS BIGINT)        AS pop0,
    TRY_CAST(AREA1 AS BIGINT)       AS area1,
    TRY_CAST(POP1 AS BIGINT)        AS pop1,
    TRY_CAST(AREA2 AS BIGINT)       AS area2,
    TRY_CAST(POP2 AS BIGINT)        AS pop2,
    TRY_CAST(AREA3 AS BIGINT)       AS area3,
    TRY_CAST(POP3 AS BIGINT)        AS pop3,
    TRY_CAST(AREA4 AS BIGINT)       AS area4,
    TRY_CAST(POP4 AS BIGINT)        AS pop4,
    STORM_ID                        AS storm_id,
    TRY_CAST(REGION_CODE AS INT)    AS region_code,
    TRY_CAST(YEAR AS INT)           AS year,
    TRY_CAST(MONTH AS INT)          AS month
FROM "noaa-regional-snowfall-index"
WHERE STORM_ID IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY STORM_ID, REGION_CODE ORDER BY YEAR) = 1
