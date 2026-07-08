SELECT
    country_l2 AS country,
    sector,
    CAST(year AS INTEGER)  AS year,
    CAST(value AS BIGINT)  AS employment
FROM "cedefop-country-sectors"
WHERE value IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY country_l2, sector, year ORDER BY value DESC) = 1
