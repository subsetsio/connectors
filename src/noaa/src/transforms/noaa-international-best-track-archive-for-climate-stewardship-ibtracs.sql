SELECT
    SID                                    AS sid,
    TRY_CAST(SEASON AS INT)                AS season,
    TRY_CAST(NUMBER AS INT)                AS storm_number,
    BASIN                                  AS basin,
    SUBBASIN                               AS subbasin,
    NAME                                   AS name,
    TRY_CAST(ISO_TIME AS TIMESTAMP)        AS iso_time,
    NATURE                                 AS nature,
    TRY_CAST(LAT AS DOUBLE)                AS lat,
    TRY_CAST(LON AS DOUBLE)                AS lon,
    TRY_CAST(WMO_WIND AS INT)              AS wmo_wind,
    TRY_CAST(WMO_PRES AS INT)              AS wmo_pres,
    TRY_CAST(DIST2LAND AS INT)             AS dist2land,
    TRY_CAST(LANDFALL AS INT)              AS landfall,
    TRY_CAST(USA_WIND AS INT)              AS usa_wind,
    TRY_CAST(USA_PRES AS INT)              AS usa_pres,
    TRY_CAST(USA_SSHS AS INT)              AS usa_sshs
FROM "noaa-international-best-track-archive-for-climate-stewardship-ibtracs"
WHERE TRY_CAST(ISO_TIME AS TIMESTAMP) IS NOT NULL AND SID IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY SID, ISO_TIME ORDER BY SID) = 1
