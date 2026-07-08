SELECT table_title,
       row_label,
       period,
       metric,
       CAST(value AS DOUBLE) AS value
FROM "fca-retirement-income-market"
WHERE value IS NOT NULL AND row_label IS NOT NULL
