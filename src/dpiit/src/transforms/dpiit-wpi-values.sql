SELECT
    item_code,
    item_name,
    CAST(weight AS DOUBLE) AS weight,
    base_year,
    CAST(date AS DATE) AS date,
    CAST(index_value AS DOUBLE) AS index_value
FROM "dpiit-wpi-values"
WHERE index_value IS NOT NULL
