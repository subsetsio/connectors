SELECT
    country,
    species,
    survey_type,
    term,
    TRY_CAST(average_number_of_sites AS INTEGER) AS average_number_of_sites,
    TRY_CAST(trend_pct_change AS DOUBLE)         AS trend_pct_change,
    TRY_CAST(lower_confidence_limit AS DOUBLE)   AS lower_confidence_limit,
    TRY_CAST(upper_confidence_limit AS DOUBLE)   AS upper_confidence_limit,
    significance_of_change
FROM "nbmp-population-trends"
WHERE term IS NOT NULL
  AND species IS NOT NULL
  AND country IS NOT NULL
