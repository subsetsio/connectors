SELECT
    collision_index,
    TRY_CAST(collision_year AS INTEGER)              AS collision_year,
    TRY_CAST(location_easting_osgr AS INTEGER)       AS location_easting_osgr,
    TRY_CAST(location_northing_osgr AS INTEGER)      AS location_northing_osgr,
    TRY_CAST(longitude AS DOUBLE)                    AS longitude,
    TRY_CAST(latitude AS DOUBLE)                     AS latitude,
    TRY_CAST(police_force AS INTEGER)                AS police_force,
    TRY_CAST(collision_severity AS INTEGER)          AS collision_severity,
    TRY_CAST(number_of_vehicles AS INTEGER)          AS number_of_vehicles,
    TRY_CAST(number_of_casualties AS INTEGER)        AS number_of_casualties,
    TRY_STRPTIME(date, '%d/%m/%Y')::DATE             AS collision_date,
    TRY_CAST(day_of_week AS INTEGER)                 AS day_of_week,
    time,
    local_authority_district,
    TRY_CAST(speed_limit AS INTEGER)                 AS speed_limit,
    TRY_CAST(light_conditions AS INTEGER)            AS light_conditions,
    TRY_CAST(weather_conditions AS INTEGER)          AS weather_conditions,
    TRY_CAST(road_surface_conditions AS INTEGER)     AS road_surface_conditions
FROM "uk-dft-road-accidents-safety-data"
WHERE collision_index IS NOT NULL
