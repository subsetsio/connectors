SELECT
    survey_id,
    question_code,
    country,
    answer,
    CAST(weighted_n AS DOUBLE) AS weighted_n,
    CAST(share AS DOUBLE)      AS share
FROM "eurobarometer-responses"
WHERE country IS NOT NULL
  AND country <> '-'              -- stray empty banner-column header
  AND answer IS NOT NULL
  AND (weighted_n IS NOT NULL OR share IS NOT NULL)
