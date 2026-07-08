SELECT
    series_id,
    parameter,
    label,
    location_identifier,
    location_name,
    location_type,
    watershed,
    CAST(latitude  AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    TRY_CAST(start_time AS TIMESTAMP) AS start_time,
    TRY_CAST(end_time   AS TIMESTAMP) AS end_time,
    CAST(timezone AS DOUBLE) AS utc_offset_hours
FROM "panama-canal-authority-series"
WHERE series_id IS NOT NULL
