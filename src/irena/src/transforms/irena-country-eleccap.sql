SELECT CAST(year AS INTEGER) AS year, country, technology, grid_connection, CAST(value AS DOUBLE) AS value, 'MW' AS unit FROM "irena-country-eleccap" WHERE value IS NOT NULL
