SELECT survey_date, variable, horizon, measure, value
FROM "philadelphia-fed-spf-dispersion"
WHERE value IS NOT NULL
ORDER BY survey_date, variable, horizon, measure
