SELECT
    account_category,
    TRY_CAST(fy_2013 AS DOUBLE) AS fy_2013,
    TRY_CAST(fy_2012 AS DOUBLE) AS fy_2012
FROM "port-of-la-jdgw-bwcf"
WHERE account_category IS NOT NULL
