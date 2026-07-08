SELECT
    country,
    country_code,
    CAST(date || '-01' AS DATE) AS date,
    * EXCLUDE (country, country_code, date)
FROM "treasury-tic-slt2-foreign-lt-securities-held-by-us-residents"
WHERE date IS NOT NULL
