-- the API returns year=null for every mitigation-potential row (these are
-- static potential estimates, not time-indexed); year column dropped.
SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    indicator,
    category,
    CAST(value AS DOUBLE) AS value
FROM "global-mangrove-watch-mitigation-potentials"
WHERE value IS NOT NULL
