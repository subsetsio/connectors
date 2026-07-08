SELECT
    country_l2 AS country,
    qualification,
    CAST(year AS INTEGER)  AS year,
    CAST(value AS BIGINT)  AS labour_force
FROM "cedefop-country-labour-force-by-qualification"
WHERE value IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY country_l2, qualification, year ORDER BY value DESC) = 1
