SELECT
    CAST(category AS VARCHAR) AS category,
    CAST(series   AS VARCHAR) AS series,
    CAST(value    AS DOUBLE)  AS value
FROM "ofgem-176999"
WHERE value IS NOT NULL
