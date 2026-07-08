SELECT
    TRIM(StationNumber)                              AS station_number,
    TRIM(StationName)                                AS station_name,
    TRIM(StationType)                                AS station_type,
    TRIM(State)                                      AS state,
    TRIM(County)                                     AS county,
    TRIM(City)                                       AS city,
    TRY_CAST(TRIM(Latitude) AS DOUBLE)               AS latitude,
    TRY_CAST(TRIM(Longitude) AS DOUBLE)              AS longitude,
    TRY_CAST(TRIM(Elevation) AS DOUBLE)              AS elevation_ft,
    TRIM(StationStatus)                              AS status,
    TRY(strptime(TRIM(CreationDate), '%Y-%m-%d %I:%M %p'))       AS created_at,
    TRY(strptime(TRIM(DateTimeStamp), '%Y-%m-%d %I:%M %p'))      AS updated_at
FROM "cocorahs-stations"
WHERE TRIM(StationNumber) IS NOT NULL AND TRIM(StationNumber) <> ''
