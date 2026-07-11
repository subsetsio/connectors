SELECT
    name,
    country,
    CAST(latitude AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    CAST(time AS TIMESTAMP) AS time,
    CAST(wave_height AS DOUBLE) AS wave_height,
    CAST(wave_period AS DOUBLE) AS wave_period,
    CAST(wave_direction AS DOUBLE) AS wave_direction
FROM "open-meteo-marine"
