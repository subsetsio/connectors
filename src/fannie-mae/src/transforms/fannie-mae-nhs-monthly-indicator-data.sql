SELECT
    CAST(date AS DATE)        AS date,
    CAST(category AS VARCHAR) AS category,
    CAST(indicator AS VARCHAR) AS indicator,
    CAST(value AS DOUBLE)     AS value
FROM "fannie-mae-nhs-monthly-indicator-data"
WHERE value IS NOT NULL
