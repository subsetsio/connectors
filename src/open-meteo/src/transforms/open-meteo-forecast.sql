SELECT
    name,
    country,
    CAST(latitude AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    CAST(date AS DATE) AS date,
    CAST(temperature_2m_max AS DOUBLE) AS temperature_2m_max,
    CAST(temperature_2m_min AS DOUBLE) AS temperature_2m_min,
    CAST(precipitation_sum AS DOUBLE) AS precipitation_sum
FROM "open-meteo-forecast"
