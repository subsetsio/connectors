SELECT
    CAST(local_authority_id AS BIGINT)      AS local_authority_id,
    local_authority_name,
    local_authority_code,
    CAST(year AS INTEGER)                    AS year,
    TRY_CAST(link_length_km AS DOUBLE)       AS link_length_km,
    TRY_CAST(link_length_miles AS DOUBLE)    AS link_length_miles,
    TRY_CAST(cars_and_taxis AS DOUBLE)       AS cars_and_taxis,
    TRY_CAST(all_motor_vehicles AS DOUBLE)   AS all_motor_vehicles
FROM "uk-dft-gb-road-traffic-counts"
WHERE year IS NOT NULL
