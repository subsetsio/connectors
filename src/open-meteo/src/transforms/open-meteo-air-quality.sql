SELECT
    name,
    country,
    CAST(latitude AS DOUBLE)  AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    CAST(time AS TIMESTAMP)   AS time,
    CAST(pm10 AS DOUBLE) AS pm10,
    CAST(pm2_5 AS DOUBLE) AS pm2_5,
    CAST(ozone AS DOUBLE) AS ozone
FROM "open-meteo-air-quality"
