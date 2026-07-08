SELECT station,
       CAST(date AS DATE)            AS date,
       CAST(decimal_date AS DOUBLE)  AS decimal_date,
       CAST(n_flasks AS INTEGER)     AS n_flasks,
       CAST(flag AS INTEGER)         AS flag,
       CAST(value AS DOUBLE)         AS value
FROM "scripps-co2-daily-merge-co2"
WHERE value IS NOT NULL AND CAST(flag AS INTEGER) <= 0
