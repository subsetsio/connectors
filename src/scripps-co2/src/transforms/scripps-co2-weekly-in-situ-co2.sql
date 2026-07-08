SELECT station,
       CAST(date AS DATE)    AS date,
       CAST(value AS DOUBLE) AS value
FROM "scripps-co2-weekly-in-situ-co2"
WHERE value IS NOT NULL
