SELECT
    CAST(date AS DATE)    AS date,
    CAST(value AS DOUBLE) AS value,
    * EXCLUDE (date, value)
FROM "afdb-vomwoge"
WHERE value IS NOT NULL
