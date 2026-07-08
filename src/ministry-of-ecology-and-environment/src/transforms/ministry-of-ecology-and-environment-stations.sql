SELECT DISTINCT
    CAST(StationCode AS VARCHAR)        AS station_code,
    CAST(PositionName AS VARCHAR)       AS station_name,
    CAST(Area AS VARCHAR)               AS area,
    TRY_CAST(CityCode AS INTEGER)       AS city_code,
    TRY_CAST(ProvinceId AS INTEGER)     AS province_id,
    TRY_CAST(Latitude AS DOUBLE)        AS latitude,
    TRY_CAST(Longitude AS DOUBLE)       AS longitude
FROM "ministry-of-ecology-and-environment-stations"
WHERE StationCode IS NOT NULL
