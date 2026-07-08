SELECT
    iso3,
    country_name,
    CAST(year AS INTEGER) AS year,
    CAST(conflict_new_displacement AS BIGINT) AS conflict_new_displacement,
    CAST(conflict_new_displacement_rounded AS BIGINT) AS conflict_new_displacement_rounded,
    CAST(conflict_total_displacement AS BIGINT) AS conflict_total_displacement,
    CAST(conflict_total_displacement_rounded AS BIGINT) AS conflict_total_displacement_rounded,
    CAST(disaster_new_displacement AS BIGINT) AS disaster_new_displacement,
    CAST(disaster_new_displacement_rounded AS BIGINT) AS disaster_new_displacement_rounded,
    CAST(disaster_total_displacement AS BIGINT) AS disaster_total_displacement,
    CAST(disaster_total_displacement_rounded AS BIGINT) AS disaster_total_displacement_rounded
FROM "idmc-displacements"
WHERE iso3 IS NOT NULL AND year IS NOT NULL
