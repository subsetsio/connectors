SELECT
    CAST(date AS DATE)    AS date,
    CAST(value AS DOUBLE) AS value,
    * EXCLUDE (date, value)
FROM "afdb-onszrad"
WHERE value IS NOT NULL
