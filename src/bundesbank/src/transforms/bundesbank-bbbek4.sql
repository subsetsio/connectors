SELECT
    CASE
        WHEN regexp_matches(time_period, '^\d{4}$')
            THEN make_date(CAST(time_period AS INT), 1, 1)
        WHEN regexp_matches(time_period, '^\d{4}-\d{2}$')
            THEN make_date(
                CAST(time_period[1:4] AS INT),
                CAST(time_period[6:7] AS INT), 1)
        WHEN regexp_matches(time_period, '^\d{4}-\d{2}-\d{2}$')
            THEN CAST(time_period AS DATE)
        WHEN regexp_matches(time_period, '^\d{4}-Q[1-4]$')
            THEN make_date(
                CAST(time_period[1:4] AS INT),
                (CAST(time_period[7:7] AS INT) - 1) * 3 + 1, 1)
        WHEN regexp_matches(time_period, '^\d{4}-S[1-2]$')
            THEN make_date(
                CAST(time_period[1:4] AS INT),
                (CAST(time_period[7:7] AS INT) - 1) * 6 + 1, 1)
        WHEN regexp_matches(time_period, '^\d{4}-W\d{2}$')
            THEN make_date(CAST(time_period[1:4] AS INT), 1, 1)
                + ((CAST(time_period[7:8] AS INT) - 1) * 7)
        ELSE NULL
    END AS date,
    time_period,
    time_format AS frequency,
    series_id,
    title,
    unit,
    value
FROM "bundesbank-bbbek4"
WHERE value IS NOT NULL
  AND time_period IS NOT NULL
