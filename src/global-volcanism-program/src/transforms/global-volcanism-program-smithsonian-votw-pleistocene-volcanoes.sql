SELECT
    * EXCLUDE (Volcano_Number, Latitude, Longitude, Elevation),
    TRY_CAST(Volcano_Number AS BIGINT) AS Volcano_Number,
    TRY_CAST(Latitude AS DOUBLE)       AS Latitude,
    TRY_CAST(Longitude AS DOUBLE)      AS Longitude,
    TRY_CAST(Elevation AS DOUBLE)      AS Elevation
FROM "global-volcanism-program-smithsonian-votw-pleistocene-volcanoes"
