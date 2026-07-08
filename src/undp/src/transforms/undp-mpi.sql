SELECT
    country,
    survey,
    CAST(mpi_value AS DOUBLE) AS mpi_value,
    CAST(headcount_pct AS DOUBLE) AS headcount_pct,
    CAST(pop_poor_survey_thousands AS DOUBLE) AS pop_poor_survey_thousands,
    CAST(pop_poor_2023_thousands AS DOUBLE) AS pop_poor_2023_thousands,
    CAST(intensity_pct AS DOUBLE) AS intensity_pct,
    CAST(inequality AS DOUBLE) AS inequality,
    CAST(severe_poverty_pct AS DOUBLE) AS severe_poverty_pct,
    CAST(vulnerable_pct AS DOUBLE) AS vulnerable_pct,
    CAST(contrib_health_pct AS DOUBLE) AS contrib_health_pct,
    CAST(contrib_education_pct AS DOUBLE) AS contrib_education_pct,
    CAST(contrib_living_standards_pct AS DOUBLE) AS contrib_living_standards_pct,
    CAST(national_poverty_pct AS DOUBLE) AS national_poverty_pct,
    CAST(ppp300_poverty_pct AS DOUBLE) AS ppp300_poverty_pct
FROM "undp-mpi"
WHERE mpi_value IS NOT NULL
