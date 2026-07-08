SELECT period, gdpplus AS gdpplus_growth
FROM (
    SELECT period, gdpplus,
           row_number() OVER (PARTITION BY period ORDER BY vintage_date DESC) AS rn
    FROM "philadelphia-fed-gdpplus"
    WHERE gdpplus IS NOT NULL
)
WHERE rn = 1
ORDER BY period
