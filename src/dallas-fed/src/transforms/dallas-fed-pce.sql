SELECT DISTINCT
    CAST(date AS DATE)       AS date,
    CAST(horizon AS VARCHAR) AS horizon,
    CAST(value AS DOUBLE)    AS value
FROM "dallas-fed-pce"
WHERE date IS NOT NULL AND value IS NOT NULL
