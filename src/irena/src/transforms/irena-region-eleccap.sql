SELECT CAST(year AS INTEGER) AS year, region, technology, grid_connection, CAST(value AS DOUBLE) AS value, 'MW' AS unit FROM "irena-region-eleccap" WHERE value IS NOT NULL
