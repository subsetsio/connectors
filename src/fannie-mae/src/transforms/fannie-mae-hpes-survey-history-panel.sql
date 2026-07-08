SELECT
    CAST(metric AS VARCHAR)        AS metric,
    CAST(survey_year AS INTEGER)   AS survey_year,
    CAST(survey_period AS VARCHAR) AS survey_period,
    CAST(target_year AS INTEGER)   AS target_year,
    CAST(value AS DOUBLE)          AS value
FROM "fannie-mae-hpes-survey-history-panel"
WHERE value IS NOT NULL
