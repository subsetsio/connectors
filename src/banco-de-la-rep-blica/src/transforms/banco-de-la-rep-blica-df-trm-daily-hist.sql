SELECT
    CASE
        WHEN regexp_full_match(time_period, '^[0-9]{8}$')
            THEN make_date(
                CAST(substr(time_period, 1, 4) AS INT),
                CAST(substr(time_period, 5, 2) AS INT),
                CAST(substr(time_period, 7, 2) AS INT))
        WHEN regexp_full_match(time_period, '^[0-9]{4}-[0-9]{2}$')
            THEN make_date(
                CAST(substr(time_period, 1, 4) AS INT),
                CAST(substr(time_period, 6, 2) AS INT), 1)
        WHEN regexp_full_match(time_period, '^[0-9]{4}-Q[1-4]$')
            THEN make_date(
                CAST(substr(time_period, 1, 4) AS INT),
                (CAST(substr(time_period, 7, 1) AS INT) - 1) * 3 + 1, 1)
        WHEN regexp_full_match(time_period, '^[0-9]{4}$')
            THEN make_date(CAST(time_period AS INT), 1, 1)
    END AS date,
    subject,
    reference_area,
    unit_measure,
    adjustment,
    freq,
    TRY_CAST(unit_mult AS INTEGER) AS unit_mult,
    TRY_CAST(obs_value AS DOUBLE)  AS value,
    obs_status
FROM "banco-de-la-rep-blica-df-trm-daily-hist"
WHERE obs_value IS NOT NULL
  AND TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
  AND time_period IS NOT NULL
  AND CASE
        WHEN regexp_full_match(time_period, '^[0-9]{8}$') THEN TRUE
        WHEN regexp_full_match(time_period, '^[0-9]{4}-[0-9]{2}$') THEN TRUE
        WHEN regexp_full_match(time_period, '^[0-9]{4}-Q[1-4]$') THEN TRUE
        WHEN regexp_full_match(time_period, '^[0-9]{4}$') THEN TRUE
        ELSE FALSE
      END
