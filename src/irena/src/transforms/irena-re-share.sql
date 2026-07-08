SELECT CAST(year AS INTEGER) AS year, region, indicator, CAST(value AS DOUBLE) AS value, '%' AS unit FROM "irena-re-share" WHERE value IS NOT NULL
