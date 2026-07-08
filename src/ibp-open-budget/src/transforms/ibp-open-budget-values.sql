SELECT DISTINCT
    indicator_code,
    ref_area                         AS country_iso3,
    CAST(time_period AS INTEGER)     AS year,
    CAST(obs_value AS DOUBLE)        AS value,
    unit_measure
FROM "ibp-open-budget-values"
WHERE obs_value IS NOT NULL
  AND obs_value <> ''
  AND lower(obs_value) <> 'nan'
  AND time_period IS NOT NULL
