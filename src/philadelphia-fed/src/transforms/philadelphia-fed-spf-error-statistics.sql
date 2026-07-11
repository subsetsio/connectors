SELECT variable, date, series, horizon, value
FROM "philadelphia-fed-spf-error-statistics"
WHERE value IS NOT NULL
ORDER BY variable, date, series, horizon
