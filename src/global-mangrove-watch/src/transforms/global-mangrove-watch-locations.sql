SELECT
    CAST(id AS BIGINT)              AS location_id,
    location_uuid,
    iso,
    location_type,
    name                           AS location_name,
    TRY_CAST(area_m2 AS DOUBLE)        AS area_m2,
    TRY_CAST(coast_length_m AS DOUBLE) AS coast_length_m,
    TRY_CAST(perimeter_m AS DOUBLE)    AS perimeter_m
FROM "global-mangrove-watch-locations"
