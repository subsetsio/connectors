SELECT DISTINCT
    theme,
    sub_theme,
    topic,
    geography_type,
    metric
FROM "ukhsa-metrics"
WHERE metric IS NOT NULL
