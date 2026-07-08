SELECT
    country_code,
    country_name,
    series_code,
    series_name,
    time_label,
    CAST(substr(time_label, 1, 4) AS INTEGER)                       AS year,
    CAST(substr(time_label, 6, 1) AS INTEGER)                       AS quarter,
    make_date(
        CAST(substr(time_label, 1, 4) AS INTEGER),
        (CAST(substr(time_label, 6, 1) AS INTEGER) - 1) * 3 + 1,
        1
    )                                                               AS period_start,
    CAST(value AS DOUBLE)                                           AS value
FROM "joint-external-debt-hub-values"
WHERE value IS NOT NULL
  AND country_code IS NOT NULL
  AND time_label IS NOT NULL
  AND regexp_full_match(time_label, '[0-9]{4}Q[1-4]')
