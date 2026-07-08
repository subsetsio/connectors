SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    category,
    label,
    CAST(value AS DOUBLE)      AS value,
    CAST(percentage AS DOUBLE) AS percentage
FROM "global-mangrove-watch-blue-carbon-investment"
WHERE value IS NOT NULL
