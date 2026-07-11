SELECT
    series_key,
    obs_index,
    date AS period,
    CASE
        WHEN length(date) = 4  THEN try_strptime(date || '-01-01', '%Y-%m-%d')
        WHEN length(date) = 7  THEN try_strptime(date || '-01', '%Y-%m-%d')
        ELSE                        try_strptime(date, '%Y-%m-%d')
    END::DATE AS date,
    CAST(value AS DOUBLE) AS value
FROM "kof-ds-kmi-mixed-freq"
WHERE value IS NOT NULL
