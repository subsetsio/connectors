SELECT
    name,
    country,
    CAST(latitude AS DOUBLE)  AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    model,
    CAST(date AS DATE)        AS date,
    CAST(temperature_2m_max AS DOUBLE) AS temperature_2m_max
FROM "open-meteo-climate-projections"
