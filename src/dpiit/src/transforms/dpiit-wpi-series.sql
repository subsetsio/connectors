SELECT
    item_code,
    item_name,
    CAST(weight AS DOUBLE) AS weight,
    base_year
FROM "dpiit-wpi-series"
WHERE item_code IS NOT NULL
