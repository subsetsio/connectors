SELECT
    notation,
    label,
    river_name,
    TRY_CAST(lat AS DOUBLE)      AS lat,
    TRY_CAST(long AS DOUBLE)     AS lon,
    TRY_CAST(easting AS DOUBLE)  AS easting,
    TRY_CAST(northing AS DOUBLE) AS northing,
    TRY_CAST(date_opened AS DATE) AS date_opened,
    station_guid,
    wiski_id
FROM "defra-hydrology-stations"
WHERE notation IS NOT NULL AND notation <> ''
