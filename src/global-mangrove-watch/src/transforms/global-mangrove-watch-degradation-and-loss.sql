SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    indicator,
    label,
    CAST(value AS DOUBLE) AS value
FROM "global-mangrove-watch-degradation-and-loss"
WHERE value IS NOT NULL
