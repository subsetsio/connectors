SELECT
    CAST(country AS VARCHAR)              AS country_code,
    CAST(country_name AS VARCHAR)         AS country_name,
    CAST(indicator AS VARCHAR)            AS indicator_code,
    CAST(indicator_name AS VARCHAR)       AS indicator_name,
    CAST(classification AS VARCHAR)       AS classification_code,
    CAST(classification_name AS VARCHAR)  AS classification_name,
    CAST(classification_combo AS VARCHAR) AS classification_combo_code,
    CAST(classification_combo_name AS VARCHAR) AS classification_combo_name,
    CAST(time_period AS INTEGER)          AS year,
    CAST(value AS DOUBLE)                 AS value
FROM "unido-sdg"
WHERE value IS NOT NULL
