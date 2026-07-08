SELECT section,
       table_title,
       CAST(year AS INTEGER) AS year,
       metric,
       CAST(value AS DOUBLE) AS value
FROM "fca-retail-intermediary-market"
WHERE value IS NOT NULL AND year IS NOT NULL
