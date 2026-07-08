SELECT CAST(year AS INTEGER) AS year, country, technology, data_type, grid_connection, CAST(value AS DOUBLE) AS value, 'GWh' AS unit FROM "irena-country-elecgen" WHERE value IS NOT NULL
