SELECT DISTINCT
    CAST(date AS DATE)        AS date,
    CAST(segment AS VARCHAR)  AS segment,
    CAST(basis AS VARCHAR)    AS basis,
    CAST(series_code AS VARCHAR) AS series_code,
    CAST(component AS VARCHAR) AS component,
    CAST(value AS DOUBLE)     AS value
FROM "dallas-fed-tmos"
WHERE date IS NOT NULL AND value IS NOT NULL
