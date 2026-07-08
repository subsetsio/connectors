SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    indicator,
    indicator_type,
    CAST(value AS DOUBLE) AS value
FROM "global-mangrove-watch-fishery-mitigation-potentials"
WHERE value IS NOT NULL
