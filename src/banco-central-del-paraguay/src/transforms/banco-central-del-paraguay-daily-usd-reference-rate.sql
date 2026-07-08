SELECT
    CAST(date AS DATE)  AS date,
    guaranies_per_usd
FROM "banco-central-del-paraguay-daily-usd-reference-rate"
WHERE guaranies_per_usd IS NOT NULL
