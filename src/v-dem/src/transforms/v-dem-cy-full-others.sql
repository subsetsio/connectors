WITH long AS (
    UNPIVOT "v-dem-cy-full-others"
    ON COLUMNS(* EXCLUDE (country_name, country_text_id, country_id, year, historical_date))
    INTO NAME variable VALUE value
)
SELECT
    country_name,
    country_text_id,
    TRY_CAST(country_id AS INTEGER)   AS country_id,
    TRY_CAST(year AS INTEGER)         AS year,
    TRY_CAST(historical_date AS DATE) AS date,
    variable,
    TRY_CAST(value AS DOUBLE)         AS value
FROM long
WHERE value IS NOT NULL
  AND value <> ''
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
  AND (
        starts_with(variable, 'v2')
     OR starts_with(variable, 'v3')
     OR starts_with(variable, 'e_')
  )
