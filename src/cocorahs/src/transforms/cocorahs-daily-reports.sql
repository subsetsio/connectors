SELECT
    TRIM(StationNumber)                              AS station_number,
    TRIM(StationName)                                AS station_name,
    TRIM(State)                                      AS state,
    TRY_CAST(TRIM(ObservationDate) AS DATE)          AS observation_date,
    TRIM(ObservationTime)                            AS observation_time,
    TRY_CAST(TRIM(Latitude) AS DOUBLE)               AS latitude,
    TRY_CAST(TRIM(Longitude) AS DOUBLE)              AS longitude,
    TRY_CAST(TRIM(TotalPrecipAmt) AS DOUBLE)         AS total_precip_in,
    TRY_CAST(TRIM(NewSnowDepth) AS DOUBLE)           AS new_snow_in,
    TRY_CAST(TRIM(NewSnowSWE) AS DOUBLE)             AS new_snow_swe_in,
    TRY_CAST(TRIM(TotalSnowDepth) AS DOUBLE)         AS total_snow_depth_in,
    TRY_CAST(TRIM(TotalSnowSWE) AS DOUBLE)           AS total_snow_swe_in,
    TRIM(Flooding)                                   AS flooding,
    NULLIF(TRIM(Notes), '')                          AS notes,
    TRY(strptime(TRIM(DateTimeStamp), '%Y-%m-%d %I:%M %p'))      AS updated_at
FROM "cocorahs-daily-reports"
WHERE TRY_CAST(TRIM(ObservationDate) AS DATE) IS NOT NULL
