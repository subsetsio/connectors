SELECT
    CAST(period AS DATE) AS date,
    sheet,
    series,
    CAST(value AS DOUBLE) AS value
FROM (
    SELECT *, row_number() OVER (
        PARTITION BY period, sheet, series ORDER BY value DESC
    ) AS _rn
    FROM "nhs-england-ae-waiting-times-and-activity"
)
WHERE _rn = 1
  AND period IS NOT NULL
  AND value IS NOT NULL
