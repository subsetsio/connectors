SELECT
    name,
    country,
    CAST(latitude AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude
FROM "open-meteo-locations"
