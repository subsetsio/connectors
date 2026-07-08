SELECT
    country,
    country_code,
    CAST(date || '-01' AS DATE) AS date,
    * EXCLUDE (country, country_code, date)
FROM "treasury-tic-slt1-us-lt-securities-held-by-foreign-residents"
WHERE date IS NOT NULL
