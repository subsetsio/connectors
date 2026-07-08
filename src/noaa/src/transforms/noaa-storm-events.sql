SELECT
    TRY_CAST(EVENT_ID AS BIGINT)                            AS event_id,
    TRY_CAST(EPISODE_ID AS BIGINT)                          AS episode_id,
    make_date(
        CAST(substr(BEGIN_YEARMONTH, 1, 4) AS INT),
        CAST(substr(BEGIN_YEARMONTH, 5, 2) AS INT),
        TRY_CAST(BEGIN_DAY AS INT)
    )                                                       AS begin_date,
    BEGIN_TIME                                              AS begin_time,
    TRY_CAST(YEAR AS INT)                                   AS year,
    MONTH_NAME                                              AS month_name,
    STATE                                                   AS state,
    TRY_CAST(STATE_FIPS AS INT)                             AS state_fips,
    EVENT_TYPE                                              AS event_type,
    CZ_TYPE                                                 AS cz_type,
    CZ_NAME                                                 AS cz_name,
    WFO                                                     AS wfo,
    TRY_CAST(INJURIES_DIRECT AS INT)                        AS injuries_direct,
    TRY_CAST(INJURIES_INDIRECT AS INT)                      AS injuries_indirect,
    TRY_CAST(DEATHS_DIRECT AS INT)                          AS deaths_direct,
    TRY_CAST(DEATHS_INDIRECT AS INT)                        AS deaths_indirect,
    DAMAGE_PROPERTY                                         AS damage_property,
    DAMAGE_CROPS                                            AS damage_crops,
    TRY_CAST(MAGNITUDE AS DOUBLE)                           AS magnitude,
    MAGNITUDE_TYPE                                          AS magnitude_type,
    TOR_F_SCALE                                             AS tor_f_scale,
    TRY_CAST(BEGIN_LAT AS DOUBLE)                           AS begin_lat,
    TRY_CAST(BEGIN_LON AS DOUBLE)                           AS begin_lon,
    TRY_CAST(END_LAT AS DOUBLE)                             AS end_lat,
    TRY_CAST(END_LON AS DOUBLE)                             AS end_lon,
    SOURCE                                                  AS source,
    FLOOD_CAUSE                                             AS flood_cause
FROM "noaa-storm-events"
WHERE TRY_CAST(EVENT_ID AS BIGINT) IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY EVENT_ID ORDER BY BEGIN_YEARMONTH) = 1
