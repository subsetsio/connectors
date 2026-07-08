SELECT
    region,
    country,
    CAST(year AS INTEGER) AS year,
    national_democratic_governance,
    electoral_process,
    civil_society,
    independent_media,
    local_democratic_governance,
    judicial_framework_and_independence,
    corruption,
    democracy_score,
    democracy_percentage,
    democracy_percentage_rounded,
    regime_classification
FROM "freedom-house-nations-in-transit"
WHERE country IS NOT NULL AND year IS NOT NULL
