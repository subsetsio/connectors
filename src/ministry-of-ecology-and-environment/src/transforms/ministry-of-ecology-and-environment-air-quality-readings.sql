SELECT
    CAST(StationCode AS VARCHAR)              AS station_code,
    to_timestamp(time_ms / 1000.0)           AS observed_at,
    TRY_CAST(AQI AS INTEGER)                  AS aqi,
    NULLIF(NULLIF(NULLIF(CAST(Quality AS VARCHAR), ''), 'NA'), '—')          AS quality,
    NULLIF(NULLIF(NULLIF(CAST(PrimaryPollutant AS VARCHAR), ''), 'NA'), '—') AS primary_pollutant,
    TRY_CAST(PM2_5 AS DOUBLE)                 AS pm2_5,
    TRY_CAST(PM2_5_24h AS DOUBLE)             AS pm2_5_24h,
    TRY_CAST(PM10 AS DOUBLE)                  AS pm10,
    TRY_CAST(PM10_24h AS DOUBLE)              AS pm10_24h,
    TRY_CAST(SO2 AS DOUBLE)                   AS so2,
    TRY_CAST(SO2_24h AS DOUBLE)               AS so2_24h,
    TRY_CAST(NO2 AS DOUBLE)                   AS no2,
    TRY_CAST(NO2_24h AS DOUBLE)               AS no2_24h,
    TRY_CAST(O3 AS DOUBLE)                    AS o3,
    TRY_CAST(O3_24h AS DOUBLE)                AS o3_24h,
    TRY_CAST(O3_8h AS DOUBLE)                 AS o3_8h,
    TRY_CAST(O3_8h_24h AS DOUBLE)             AS o3_8h_24h,
    TRY_CAST(CO AS DOUBLE)                    AS co,
    TRY_CAST(CO_24h AS DOUBLE)                AS co_24h
FROM "ministry-of-ecology-and-environment-air-quality-readings"
WHERE StationCode IS NOT NULL AND time_ms IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY station_code, observed_at ORDER BY aqi DESC NULLS LAST
) = 1
