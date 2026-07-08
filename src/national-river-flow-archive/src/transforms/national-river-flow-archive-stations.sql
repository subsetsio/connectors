SELECT
    station_id,
    name,
    river,
    location,
    catchment_area_km2,
    easting,
    northing,
    latitude,
    longitude,
    station_level_m,
    CAST(gdf_start_date AS DATE) AS gdf_start_date,
    CAST(gdf_end_date   AS DATE) AS gdf_end_date,
    gdf_mean_flow_m3s
FROM "national-river-flow-archive-stations"
WHERE station_id IS NOT NULL
