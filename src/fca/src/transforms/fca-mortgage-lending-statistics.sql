SELECT table_sheet,
       sub_table_ref,
       metric,
       unit,
       CAST(year AS INTEGER) AS year,
       quarter,
       CAST(value AS DOUBLE) AS value
FROM "fca-mortgage-lending-statistics"
WHERE value IS NOT NULL AND metric IS NOT NULL
