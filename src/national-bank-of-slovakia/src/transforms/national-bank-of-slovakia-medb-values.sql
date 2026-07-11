SELECT
    CAST(frequency    AS VARCHAR) AS frequency,
    CAST(series_key   AS VARCHAR) AS series_key,
    CAST(classcode    AS VARCHAR) AS classcode,
    CAST(variable     AS VARCHAR) AS variable,
    CAST(detail       AS VARCHAR) AS detail,
    CAST(source       AS VARCHAR) AS source,
    CAST(period_label AS VARCHAR) AS period_label,
    CAST(date         AS DATE)    AS date,
    CAST(value        AS DOUBLE)  AS value
FROM "national-bank-of-slovakia-medb-values"
WHERE value IS NOT NULL
