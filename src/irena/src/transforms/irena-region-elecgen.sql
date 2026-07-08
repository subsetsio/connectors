SELECT CAST(year AS INTEGER) AS year, region, technology, data_type, CAST(value AS DOUBLE) AS value, 'GWh' AS unit FROM "irena-region-elecgen" WHERE value IS NOT NULL
