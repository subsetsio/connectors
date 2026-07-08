WITH base AS (
    SELECT *, TRY_CAST(acq_date AS DATE) AS d
    FROM "nasa-firms-viirs-detections"
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
    CASE lower(confidence)
        WHEN 'l' THEN 'low'
        WHEN 'n' THEN 'nominal'
        WHEN 'h' THEN 'high'
        ELSE lower(confidence)
    END                                 AS confidence,
    version,
    bright_ti4,
    bright_ti5,
    scan,
    track,
    frp,
    daynight,
    type
FROM base
WHERE latitude IS NOT NULL AND longitude IS NOT NULL AND d IS NOT NULL
