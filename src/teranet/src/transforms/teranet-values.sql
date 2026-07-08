-- An index value of 0 is never valid (base 100 = June 2005); the
-- source writes a literal 0.00 in smoothing-warmup cells where the
-- value should be absent, so NULLIF those to null. A sales_pair_count
-- of 0 is legitimate, so it is left untouched.
SELECT
    CAST("date" AS DATE)                          AS "date",
    market,
    NULLIF(CAST("index" AS DOUBLE), 0)            AS "index",
    NULLIF(CAST(sa_index AS DOUBLE), 0)          AS sa_index,
    NULLIF(CAST(smoothed_index AS DOUBLE), 0)    AS smoothed_index,
    NULLIF(CAST(smoothed_sa_index AS DOUBLE), 0) AS smoothed_sa_index,
    CAST(sales_pair_count AS BIGINT)              AS sales_pair_count
FROM "teranet-values"
WHERE "index" IS NOT NULL
   OR sa_index IS NOT NULL
   OR smoothed_index IS NOT NULL
   OR smoothed_sa_index IS NOT NULL
   OR sales_pair_count IS NOT NULL
