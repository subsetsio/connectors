SELECT
    dataflow,
    series_key,
    freq,
    time_period,
    CASE
        WHEN freq = 'D' THEN TRY_CAST(time_period AS DATE)
        WHEN freq = 'M' THEN TRY_STRPTIME(time_period || '-01', '%Y-%m-%d')::DATE
        WHEN freq = 'A' THEN TRY_STRPTIME(time_period || '-01-01', '%Y-%m-%d')::DATE
        WHEN freq = 'Q' THEN MAKE_DATE(
            TRY_CAST(SPLIT_PART(time_period, '-Q', 1) AS INTEGER),
            (TRY_CAST(SPLIT_PART(time_period, '-Q', 2) AS INTEGER) - 1) * 3 + 1,
            1)
        WHEN freq = 'H' THEN MAKE_DATE(
            TRY_CAST(SPLIT_PART(time_period, '-S', 1) AS INTEGER),
            (TRY_CAST(SPLIT_PART(time_period, '-S', 2) AS INTEGER) - 1) * 6 + 1,
            1)
        ELSE NULL
    END AS period_start,
    obs_value,
    unit_measure,
    unit_mult,
    title,
    obs_status,
    dimensions
FROM "bis-ws-lbs-d-pub"
WHERE obs_value IS NOT NULL AND isfinite(obs_value)
