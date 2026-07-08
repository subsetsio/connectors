SELECT survey_date, variable, horizon, statistic, measure, value
FROM "philadelphia-fed-spf-consensus"
WHERE value IS NOT NULL
ORDER BY survey_date, variable, horizon, statistic, measure
