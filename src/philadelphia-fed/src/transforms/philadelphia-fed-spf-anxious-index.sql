SELECT survey_date, anxious_index
FROM "philadelphia-fed-spf-anxious-index"
WHERE anxious_index IS NOT NULL
ORDER BY survey_date
