SELECT
    CAST(id AS BIGINT)                               AS observation_id,
    NULLIF(obs_type, '')                            AS obs_type,
    -- physically-impossible coords are erroneous citizen entries -> NULL
    CASE WHEN TRY_CAST(latitude AS DOUBLE) BETWEEN -90 AND 90
         THEN TRY_CAST(latitude AS DOUBLE) END       AS latitude,
    CASE WHEN TRY_CAST(longitude AS DOUBLE) BETWEEN -180 AND 180
         THEN TRY_CAST(longitude AS DOUBLE) END      AS longitude,
    CASE WHEN TRY_CAST(elevation_m AS DOUBLE) BETWEEN -500 AND 9000
         THEN TRY_CAST(elevation_m AS DOUBLE) END    AS elevation_m,
    TRY_CAST(local_date AS DATE)                    AS local_date,
    NULLIF(local_time, '')                          AS local_time,
    TRY_CAST(ut_date AS DATE)                       AS ut_date,
    NULLIF(ut_time, '')                             AS ut_time,
    EXTRACT(year FROM TRY_CAST(ut_date AS DATE))    AS year,
    -- GaN naked-eye limiting-magnitude scale is 0-7; -999/-9999 are
    -- missing-data sentinels.
    CASE WHEN TRY_CAST(limiting_mag AS INTEGER) BETWEEN 0 AND 7
         THEN TRY_CAST(limiting_mag AS INTEGER) END  AS limiting_mag,
    -- SQM night-sky brightness is ~16-22 mag/arcsec^2; 0 and absurd
    -- highs (e.g. 1e90) are bad readings.
    CASE WHEN TRY_CAST(sqm_reading AS DOUBLE) > 0
              AND TRY_CAST(sqm_reading AS DOUBLE) <= 30
         THEN TRY_CAST(sqm_reading AS DOUBLE) END    AS sqm_reading,
    NULLIF(sqm_serial, '')                          AS sqm_serial,
    NULLIF(cloud_cover, '')                         AS cloud_cover,
    NULLIF(constellation, '')                       AS constellation,
    NULLIF(sky_comment, '')                         AS sky_comment,
    NULLIF(location_comment, '')                    AS location_comment,
    NULLIF(country, '')                             AS country
FROM "globe-at-night-observations"
WHERE id IS NOT NULL AND TRY_CAST(id AS BIGINT) IS NOT NULL
