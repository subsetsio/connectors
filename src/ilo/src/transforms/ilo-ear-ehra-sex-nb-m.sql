SELECT
    make_date(TRY_CAST(substr(time_period, 1, 4) AS INTEGER), TRY_CAST(substr(time_period, 6, 2) AS INTEGER), 1) AS date,
    time_period,
    ref_area,
    source,
    sex,
    obs_value
FROM "ilo-ear-ehra-sex-nb-m"
WHERE obs_value IS NOT NULL
  AND time_period IS NOT NULL
