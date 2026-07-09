SELECT
    "SID"                            AS sid,
    CAST("SEASON" AS INTEGER)        AS season,
    CAST("NUMBER" AS INTEGER)        AS storm_number,
    "BASIN"                          AS basin,
    "SUBBASIN"                       AS subbasin,
    "NAME"                           AS name,
    CAST("ISO_TIME" AS TIMESTAMP)    AS iso_time,
    "NATURE"                         AS nature,
    CAST("LAT" AS DOUBLE)            AS lat,
    CAST("LON" AS DOUBLE)            AS lon,
    CAST("WMO_WIND" AS INTEGER)      AS wmo_wind,
    CAST("WMO_PRES" AS INTEGER)      AS wmo_pres,
    CAST("USA_WIND" AS INTEGER)      AS usa_wind,
    CAST("USA_PRES" AS INTEGER)      AS usa_pres,
    CAST("USA_SSHS" AS INTEGER)      AS usa_sshs,
    CAST("DIST2LAND" AS INTEGER)     AS dist2land,
    CAST("LANDFALL" AS INTEGER)      AS landfall
FROM "noaa-international-best-track-archive-for-climate-stewardship-ibtracs"
