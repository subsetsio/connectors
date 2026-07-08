SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    CAST(year AS INTEGER) AS year,
    indicator,
    CAST(value AS DOUBLE) AS value
FROM "global-mangrove-watch-habitat-extent"
WHERE value IS NOT NULL
