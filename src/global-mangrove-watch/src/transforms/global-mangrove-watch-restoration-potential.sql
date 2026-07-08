SELECT CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name,
    TRY_CAST(restoration_potential_score AS DOUBLE) AS restoration_potential_score,
    TRY_CAST(restorable_area AS DOUBLE)             AS restorable_area,
    TRY_CAST(restorable_area_perc AS DOUBLE)        AS restorable_area_perc,
    TRY_CAST(mangrove_area_extent AS DOUBLE)        AS mangrove_area_extent
FROM "global-mangrove-watch-restoration-potential"
