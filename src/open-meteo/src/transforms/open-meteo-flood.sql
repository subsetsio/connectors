SELECT
    name,
    country,
    CAST(latitude AS DOUBLE)  AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    CAST(date AS DATE)        AS date,
    CAST(river_discharge AS DOUBLE) AS river_discharge
FROM "open-meteo-flood"
WHERE river_discharge IS NOT NULL
