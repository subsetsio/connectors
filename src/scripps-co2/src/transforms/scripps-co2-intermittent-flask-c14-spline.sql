SELECT station,
       CAST(decimal_date AS DOUBLE) AS decimal_date,
       CAST(value AS DOUBLE)        AS value
FROM "scripps-co2-intermittent-flask-c14-spline"
WHERE value IS NOT NULL
