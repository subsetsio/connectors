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
    TRY_CAST(TRIM(TotalSnowDepth) AS DOUBLE)         AS total_snow_depth_in,
    TRIM(Flooding)                                   AS flooding,
    TRY_CAST(TRIM(PrecipDurationMin) AS DOUBLE)      AS precip_duration_min,
    TRY(strptime(TRIM(DateTimeStamp), '%Y-%m-%d %I:%M %p'))      AS updated_at
FROM "cocorahs-sigwx-reports"
WHERE TRY_CAST(TRIM(ObservationDate) AS DATE) IS NOT NULL
