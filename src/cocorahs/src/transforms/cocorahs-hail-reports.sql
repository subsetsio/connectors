SELECT
    TRIM(StationNumber)                              AS station_number,
    TRIM(StationName)                                AS station_name,
    TRIM(State)                                      AS state,
    TRY_CAST(TRIM(ObservationDate) AS DATE)          AS observation_date,
    TRIM(ObservationTime)                            AS observation_time,
    TRY_CAST(TRIM(Latitude) AS DOUBLE)               AS latitude,
    TRY_CAST(TRIM(Longitude) AS DOUBLE)              AS longitude,
    TRY_CAST(TRIM(SmallestSize) AS DOUBLE)           AS smallest_size_in,
    TRY_CAST(TRIM(AverageSize) AS DOUBLE)            AS average_size_in,
    TRY_CAST(TRIM(LargestSize) AS DOUBLE)            AS largest_size_in,
    TRY_CAST(TRIM(DurationMinutes) AS DOUBLE)        AS duration_minutes,
    TRIM(Timing)                                     AS timing,
    TRIM(StoneConsistency)                           AS stone_consistency,
    TRIM(MoreRainThanHail)                           AS more_rain_than_hail,
    TRY_CAST(TRIM(NumberOfStonesOnPad) AS DOUBLE)    AS number_of_stones_on_pad,
    TRY_CAST(TRIM(DepthOnGround) AS DOUBLE)          AS depth_on_ground_in,
    NULLIF(TRIM(Damage), '')                         AS damage,
    TRY(strptime(TRIM(EntryDateTime), '%Y-%m-%d %I:%M %p'))     AS entry_datetime,
    TRY(strptime(TRIM(DateTimeStamp), '%Y-%m-%d %I:%M %p'))      AS updated_at
FROM "cocorahs-hail-reports"
WHERE TRY_CAST(TRIM(ObservationDate) AS DATE) IS NOT NULL
