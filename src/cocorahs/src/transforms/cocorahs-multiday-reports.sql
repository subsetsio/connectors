SELECT
    TRIM(StationNumber)                              AS station_number,
    TRIM(StationName)                                AS station_name,
    TRIM(State)                                      AS state,
    TRY_CAST(TRIM(StartDate) AS DATE)                AS start_date,
    TRY(strptime(TRIM(EndDateTime), '%Y-%m-%d %I:%M %p'))        AS end_datetime,
    TRY_CAST(TRIM(Latitude) AS DOUBLE)               AS latitude,
    TRY_CAST(TRIM(Longitude) AS DOUBLE)              AS longitude,
    TRY_CAST(TRIM(TotalPrecipAmt) AS DOUBLE)         AS total_precip_in,
    TRY_CAST(TRIM(TotalSnowDepth) AS DOUBLE)         AS total_snow_depth_in,
    TRY_CAST(TRIM(TotalSnowSWE) AS DOUBLE)           AS total_snow_swe_in,
    TRY(strptime(TRIM(DateTimeStamp), '%Y-%m-%d %I:%M %p'))      AS updated_at
FROM "cocorahs-multiday-reports"
WHERE TRY_CAST(TRIM(StartDate) AS DATE) IS NOT NULL
