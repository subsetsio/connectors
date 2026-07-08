SELECT
    CAST(date AS DATE) AS date,
    year,
    month,
    metric,
    value
FROM "bundesagentur-f-r-arbeit-alo-current"
WHERE date IS NOT NULL
  AND metric IS NOT NULL
  AND value IS NOT NULL
