SELECT
    country_l2 AS country,
    gender,
    ageband,
    CAST(year AS INTEGER)  AS year,
    CAST(value AS BIGINT)  AS labour_force
FROM "cedefop-labour-force-age-gender"
WHERE value IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY country_l2, gender, ageband, year ORDER BY value DESC) = 1
