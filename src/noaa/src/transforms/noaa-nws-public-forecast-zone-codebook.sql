SELECT
    "STATE"                         AS state,
    "ZONE"                          AS zone,
    "CWA"                           AS cwa,
    "NAME"                          AS zone_name,
    "STATE_ZONE"                    AS state_zone,
    "COUNTY"                        AS county_name,
    "FIPS"                          AS county_fips,
    "TIME_ZONE"                     AS time_zone,
    "FE_AREA"                       AS feature_area,
    CAST("LAT" AS DOUBLE)           AS latitude,
    CAST("LON" AS DOUBLE)           AS longitude
FROM "noaa-nws-public-forecast-zone-codebook"
