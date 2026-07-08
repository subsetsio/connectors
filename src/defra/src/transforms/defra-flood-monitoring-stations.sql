SELECT
    notation,
    station_reference,
    label,
    river_name,
    catchment_name,
    town,
    TRY_CAST(lat AS DOUBLE)      AS lat,
    TRY_CAST(long AS DOUBLE)     AS lon,
    TRY_CAST(easting AS DOUBLE)  AS easting,
    TRY_CAST(northing AS DOUBLE) AS northing,
    TRY_CAST(date_opened AS DATE) AS date_opened,
    status,
    rloi_id
FROM "defra-flood-monitoring-stations"
WHERE notation IS NOT NULL AND notation <> ''
