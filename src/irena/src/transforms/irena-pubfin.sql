SELECT CAST(year AS INTEGER) AS year, country, technology, CAST(value AS DOUBLE) AS value, 'Million USD (2022)' AS unit FROM "irena-pubfin" WHERE value IS NOT NULL
