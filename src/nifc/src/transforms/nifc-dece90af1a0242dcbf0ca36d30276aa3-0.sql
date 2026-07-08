SELECT
    TRY_CAST(latitude AS DOUBLE)             AS latitude,
    TRY_CAST(longitude AS DOUBLE)            AS longitude,
    TRY_CAST(bright_ti4 AS DOUBLE)           AS brightness_ti4,
    TRY_CAST(bright_ti5 AS DOUBLE)           AS brightness_ti5,
    TRY_CAST(frp AS DOUBLE)                  AS fire_radiative_power,
    TRY_CAST(scan AS DOUBLE)                 AS scan,
    TRY_CAST(track AS DOUBLE)                AS track,
    CASE WHEN epoch_ms(TRY_CAST(acq_date AS BIGINT)) BETWEEN TIMESTAMP '1900-01-01' AND TIMESTAMP '2027-12-31' THEN epoch_ms(TRY_CAST(acq_date AS BIGINT)) END                        AS acquired_date,
    CASE WHEN epoch_ms(TRY_CAST(esritimeutc AS BIGINT)) BETWEEN TIMESTAMP '1900-01-01' AND TIMESTAMP '2027-12-31' THEN epoch_ms(TRY_CAST(esritimeutc AS BIGINT)) END                     AS acquired_at_utc,
    satellite                                AS satellite,
    confidence                               AS confidence,
    daynight                                 AS day_night,
    version                                  AS version,
    TRY_CAST(hours_old AS INTEGER)           AS hours_old
FROM "nifc-dece90af1a0242dcbf0ca36d30276aa3-0"
