SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    indicator,
    category,
    CAST(value AS DOUBLE) AS value
FROM "global-mangrove-watch-ecoregions"
WHERE value IS NOT NULL
