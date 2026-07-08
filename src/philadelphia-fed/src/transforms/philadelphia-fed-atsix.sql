SELECT CAST(date AS DATE) AS date,
       horizon_months,
       expected_inflation
FROM "philadelphia-fed-atsix"
WHERE expected_inflation IS NOT NULL
ORDER BY date, horizon_months
