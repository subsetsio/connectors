SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    indicator,
    category,
    TRY_CAST(year AS INTEGER) AS year,
    CAST(value AS DOUBLE)     AS value
FROM "global-mangrove-watch-fisheries"
WHERE value IS NOT NULL
