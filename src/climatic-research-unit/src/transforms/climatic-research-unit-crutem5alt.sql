SELECT
    region,
    make_date(year, month, 1) AS date,
    year,
    month,
    CAST(value AS DOUBLE)         AS value,
    CAST(station_count AS BIGINT) AS station_count
FROM "climatic-research-unit-crutem5alt"
WHERE value IS NOT NULL
