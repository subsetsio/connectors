SELECT
    country,
    country_code,
    CAST(date || '-01' AS DATE) AS date,
    * EXCLUDE (country, country_code, date)
FROM "treasury-tic-slt3-us-treasury-securities-held-by-foreign-residents"
WHERE date IS NOT NULL
