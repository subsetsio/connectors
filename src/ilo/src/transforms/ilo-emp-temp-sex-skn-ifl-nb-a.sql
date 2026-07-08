SELECT
    make_date(TRY_CAST(substr(time_period, 1, 4) AS INTEGER), 1, 1) AS date,
    time_period,
    ref_area,
    source,
    sex,
    classif1,
    classif2,
    obs_value
FROM "ilo-emp-temp-sex-skn-ifl-nb-a"
WHERE obs_value IS NOT NULL
  AND time_period IS NOT NULL
