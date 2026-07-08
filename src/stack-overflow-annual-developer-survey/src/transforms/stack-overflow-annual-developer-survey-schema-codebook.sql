SELECT
    CAST(survey_year AS INTEGER) AS survey_year,
    column_name,
    question_text
FROM "stack-overflow-annual-developer-survey-schema-codebook"
WHERE column_name IS NOT NULL
