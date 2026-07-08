SELECT CAST(survey_date AS DATE) AS survey_date,
       variable, horizon, value
FROM "philadelphia-fed-livingston-survey"
WHERE value IS NOT NULL
ORDER BY survey_date, variable, horizon
