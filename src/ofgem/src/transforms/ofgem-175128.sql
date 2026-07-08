SELECT
    CAST(category AS VARCHAR) AS category,
    CAST(series   AS VARCHAR) AS series,
    CAST(value    AS DOUBLE)  AS value
FROM "ofgem-175128"
WHERE value IS NOT NULL
