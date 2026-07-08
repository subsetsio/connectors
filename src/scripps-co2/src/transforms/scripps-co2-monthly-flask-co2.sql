SELECT station,
       CAST(year AS INTEGER)  AS year,
       CAST(month AS INTEGER) AS month,
       make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 15) AS date,
       CAST(decimal_date AS DOUBLE)                     AS decimal_date,
       CAST(value AS DOUBLE)                            AS value,
       CAST(value_seasonally_adjusted AS DOUBLE)        AS value_seasonally_adjusted,
       CAST(fit AS DOUBLE)                              AS fit,
       CAST(fit_seasonally_adjusted AS DOUBLE)          AS fit_seasonally_adjusted,
       CAST(value_filled AS DOUBLE)                     AS value_filled,
       CAST(value_filled_seasonally_adjusted AS DOUBLE) AS value_filled_seasonally_adjusted
FROM "scripps-co2-monthly-flask-co2"
WHERE value_filled IS NOT NULL
