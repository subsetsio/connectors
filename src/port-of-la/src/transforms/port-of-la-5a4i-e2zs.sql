SELECT
    CAST(year AS INTEGER) AS year,
    TRY_CAST(tons AS BIGINT) AS tons
FROM "port-of-la-5a4i-e2zs"
WHERE year IS NOT NULL
