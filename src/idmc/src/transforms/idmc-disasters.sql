SELECT
    iso3,
    country_name,
    CAST(year AS INTEGER) AS year,
    TRY_CAST(start_date AS DATE) AS start_date,
    start_date_accuracy,
    TRY_CAST(end_date AS DATE) AS end_date,
    end_date_accuracy,
    event_name,
    CAST(new_displacement AS BIGINT) AS new_displacement,
    CAST(new_displacement_rounded AS BIGINT) AS new_displacement_rounded,
    CAST(total_displacement AS BIGINT) AS total_displacement,
    CAST(total_displacement_rounded AS BIGINT) AS total_displacement_rounded,
    hazard_category_name,
    hazard_sub_category_name,
    hazard_type_name,
    hazard_sub_type_name,
    event_codes,
    event_codes_type
FROM "idmc-disasters"
WHERE iso3 IS NOT NULL AND year IS NOT NULL
