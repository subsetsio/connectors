SELECT
    accounts_category,
    TRY_CAST(as_of_march_2014 AS DOUBLE) AS as_of_march_2014,
    TRY_CAST(as_of_march_2013 AS DOUBLE) AS as_of_march_2013
FROM "port-of-la-v7gk-cxxi"
WHERE accounts_category IS NOT NULL
