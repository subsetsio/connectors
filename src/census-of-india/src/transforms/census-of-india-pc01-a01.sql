SELECT
    CAST(census_year AS INTEGER) AS census_year,
    table_code,
    source_file,
    region,
    dimensions,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "census-of-india-pc01-a01"
WHERE value IS NOT NULL
