SELECT CAST(date AS DATE)    AS date,
       CAST(value AS DOUBLE) AS value
FROM "scripps-co2-early-lajolla-co2-weekly-minima-1957-1962"
WHERE value IS NOT NULL
