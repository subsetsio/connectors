SELECT
    iso3,
    country_name,
    CAST(year AS INTEGER) AS year,
    CAST(new_displacement AS BIGINT) AS new_displacement,
    CAST(new_displacement_rounded AS BIGINT) AS new_displacement_rounded,
    CAST(total_displacement AS BIGINT) AS total_displacement,
    CAST(total_displacement_rounded AS BIGINT) AS total_displacement_rounded
FROM "idmc-conflicts"
WHERE iso3 IS NOT NULL AND year IS NOT NULL
