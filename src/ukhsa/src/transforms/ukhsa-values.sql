SELECT DISTINCT
    theme,
    sub_theme,
    topic,
    geography_type,
    geography,
    geography_code,
    metric,
    metric_group,
    stratum,
    sex,
    age,
    CAST(year AS INTEGER)            AS year,
    CAST(month AS INTEGER)           AS month,
    CAST(epiweek AS INTEGER)         AS epiweek,
    CAST(date AS DATE)               AS date,
    CAST(metric_value AS DOUBLE)     AS metric_value,
    in_reporting_delay_period
FROM "ukhsa-values"
WHERE date IS NOT NULL
  AND metric_value IS NOT NULL
