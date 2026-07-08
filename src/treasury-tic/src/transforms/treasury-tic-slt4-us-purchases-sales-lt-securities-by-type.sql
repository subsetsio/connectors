SELECT
    country,
    country_code,
    CAST(date || '-01' AS DATE) AS date,
    * EXCLUDE (country, country_code, date)
FROM "treasury-tic-slt4-us-purchases-sales-lt-securities-by-type"
WHERE date IS NOT NULL
