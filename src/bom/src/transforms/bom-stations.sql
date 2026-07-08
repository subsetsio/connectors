SELECT
    bom_station_id,
    state,
    district_code,
    station_name,
    open_date,
    close_date,
    CAST(latitude  AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude
FROM "bom-stations"
WHERE bom_station_id IS NOT NULL
