SELECT
    country,
    iso3,
    region,
    CAST(year AS INTEGER)          AS year,
    CAST(cpi_score AS DOUBLE)      AS cpi_score,
    CAST(rank AS INTEGER)          AS rank,
    CAST(num_sources AS INTEGER)   AS num_sources,
    CAST(standard_error AS DOUBLE) AS standard_error
FROM "transparency-international-cpi-timeseries"
WHERE cpi_score IS NOT NULL
