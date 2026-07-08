SELECT
    period,
    CAST(date AS DATE) AS date,
    series,
    value
FROM "central-bank-taiwan-ef35y01"
WHERE value IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY period, series ORDER BY value
) = 1
