SELECT
    CAST(date AS DATE) AS date,
    CAST(subtable AS VARCHAR) AS subtable,
    CAST(series AS VARCHAR) AS series,
    CAST(value AS DOUBLE) AS value,
    CAST(frequency AS VARCHAR) AS frequency,
    CAST(unit AS VARCHAR) AS unit
FROM "jm-boj-fs.cb.05"
WHERE value IS NOT NULL AND series IS NOT NULL
