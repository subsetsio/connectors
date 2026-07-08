SELECT
    CAST(panelist AS VARCHAR)      AS panelist,
    CAST(title AS VARCHAR)         AS title,
    CAST(affiliation AS VARCHAR)   AS affiliation,
    CAST(response_date AS DATE)    AS response_date,
    CAST(metric AS VARCHAR)        AS metric,
    CAST(forecast_year AS INTEGER) AS forecast_year,
    CAST(value AS DOUBLE)          AS value
FROM "fannie-mae-hpes-panelist-response-summary"
WHERE value IS NOT NULL
