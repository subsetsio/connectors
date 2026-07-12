SELECT
    CAST(country     AS VARCHAR) AS country,
    CAST(year        AS INTEGER) AS year,
    CAST(dimension   AS VARCHAR) AS dimension_of_inequality,
    CAST(measure     AS VARCHAR) AS measure_of_inequality,
    CAST(series_key  AS VARCHAR) AS series_key,
    CAST(series      AS INTEGER) AS series,
    CAST(description AS VARCHAR) AS description,
    CAST(value       AS DOUBLE)  AS value
FROM "chartbook-economic-inequality-dispersion-of-earnings-p90-p50-ratio"
WHERE value IS NOT NULL
