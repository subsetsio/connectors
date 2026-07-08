SELECT CAST(year AS INTEGER) AS year, country, technology, grid_connection, CAST(value AS DOUBLE) AS value, 'TJ' AS unit FROM "irena-heatgen" WHERE value IS NOT NULL
