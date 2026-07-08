SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    variable,
    primary_driver,
    CAST(value AS DOUBLE) AS value
FROM "global-mangrove-watch-drivers-of-change"
WHERE value IS NOT NULL
