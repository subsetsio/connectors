WITH long AS (
    UNPIVOT "v-dem-coder-level"
    ON COLUMNS(* EXCLUDE (country_id, country_text_id, historical_date, coder_id))
    INTO NAME variable VALUE value
)
SELECT
    country_text_id,
    country_id,
    historical_date AS date,
    coder_id,
    variable,
    TRY_CAST(value AS DOUBLE) AS value
FROM long
WHERE value IS NOT NULL
  AND value <> ''
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
  AND (
        starts_with(variable, 'v2')
     OR starts_with(variable, 'v3')
     OR starts_with(variable, 'e_')
  )
