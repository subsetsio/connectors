SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    * EXCLUDE (location_id, iso, location_type, location_name)
FROM "global-mangrove-watch-international-status"
