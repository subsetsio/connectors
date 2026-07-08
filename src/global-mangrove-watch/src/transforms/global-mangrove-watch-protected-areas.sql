SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    CAST(year AS INTEGER)          AS year,
    CAST(total_area AS DOUBLE)     AS total_area,
    CAST(protected_area AS DOUBLE) AS protected_area
FROM "global-mangrove-watch-protected-areas"
