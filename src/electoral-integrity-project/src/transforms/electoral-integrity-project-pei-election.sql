SELECT * REPLACE (
    TRY_CAST(year AS INTEGER) AS year,
    TRY_CAST(date AS DATE) AS date
)
FROM "electoral-integrity-project-pei-election"
WHERE election IS NOT NULL
