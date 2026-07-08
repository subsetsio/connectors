SELECT station,
       CAST(date AS DATE)    AS date,
       CAST(value AS DOUBLE) AS value
FROM "scripps-co2-intermittent-flask-c14"
WHERE value IS NOT NULL
