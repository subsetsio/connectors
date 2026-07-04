SELECT
    series_name                          AS series_id,
    CAST(time_period AS DATE)            AS date,
    CAST(obs_value AS DOUBLE)            AS value,
    frequency,
    unit,
    CAST(unit_mult AS DOUBLE)            AS unit_multiplier,
    NULLIF(currency, 'NA')               AS currency,
    short_description,
    long_description,
    series_attributes
FROM "federal-reserve-cp"
WHERE obs_status = 'A'
  AND obs_value IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY series_name, time_period) = 1
