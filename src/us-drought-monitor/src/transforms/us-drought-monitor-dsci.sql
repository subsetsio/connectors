SELECT
    CAST(date AS DATE)  AS date,
    region,
    CAST(dsci AS INTEGER) AS dsci
FROM "us-drought-monitor-dsci"
WHERE date IS NOT NULL AND region IS NOT NULL AND dsci IS NOT NULL
