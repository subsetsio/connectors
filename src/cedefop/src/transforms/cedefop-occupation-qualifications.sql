SELECT
    country_l2 AS country,
    occupation,
    qualification,
    CAST(year AS INTEGER)  AS year,
    CAST(value AS BIGINT)  AS employment
FROM "cedefop-occupation-qualifications"
WHERE value IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY country_l2, occupation, qualification, year ORDER BY value DESC) = 1
