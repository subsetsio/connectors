SELECT
    * EXCLUDE (period, value),
    CAST(period AS DATE)  AS date,
    CAST(value AS DOUBLE) AS value
FROM "bank-of-finland-bof-csec-publ"
WHERE value IS NOT NULL
