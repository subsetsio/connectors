SELECT
    country_l2 AS country,
    occupation,
    CAST(year AS INTEGER)  AS year,
    CAST(value AS BIGINT)  AS replacement_demand
FROM "cedefop-country-replacement-demands"
WHERE value IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY country_l2, occupation, year ORDER BY value DESC) = 1
