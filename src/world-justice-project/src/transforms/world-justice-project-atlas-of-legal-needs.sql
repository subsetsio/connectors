SELECT
    country,
    subnational_focus,
    study_name,
    implementer,
    year_polled,
    TRY_CAST(sample_size AS BIGINT) AS sample_size,
    mode,
    target_population,
    targeted_vulnerable_population,
    data_official
FROM "world-justice-project-atlas-of-legal-needs"
WHERE country IS NOT NULL
