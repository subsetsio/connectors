WITH base AS (
    SELECT *, TRY_CAST(acq_date AS DATE) AS d
    FROM "nasa-firms-modis-detections"
)
SELECT
    country,
    latitude,
    longitude,
    d                                   AS acq_date,
    acq_time,
    CAST(year(d) AS SMALLINT)           AS year,
    satellite,
    instrument,
    TRY_CAST(confidence AS SMALLINT)    AS confidence,
    version,
    brightness,
    bright_t31,
    scan,
    track,
    frp,
    daynight,
    type
FROM base
WHERE latitude IS NOT NULL AND longitude IS NOT NULL AND d IS NOT NULL
