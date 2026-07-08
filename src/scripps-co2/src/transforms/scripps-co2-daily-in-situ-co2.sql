SELECT station,
       CAST(date AS DATE)        AS date,
       CAST(value AS DOUBLE)     AS value,
       CAST(n_baseline AS INTEGER) AS n_baseline,
       CAST(scale AS VARCHAR)    AS scale
FROM "scripps-co2-daily-in-situ-co2"
WHERE value IS NOT NULL
