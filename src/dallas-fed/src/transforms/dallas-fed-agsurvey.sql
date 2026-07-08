SELECT DISTINCT
    CAST(date AS DATE)     AS date,
    CAST(topic AS VARCHAR) AS topic,
    CAST(sheet AS VARCHAR) AS sheet,
    CAST(series AS VARCHAR) AS series,
    CAST(value AS DOUBLE)  AS value
FROM "dallas-fed-agsurvey"
WHERE date IS NOT NULL AND value IS NOT NULL
