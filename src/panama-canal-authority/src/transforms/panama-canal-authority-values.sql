WITH parsed AS (
    SELECT
        series_id,
        parameter,
        label,
        location_identifier,
        watershed,
        unit,
        TRY_CAST(date AS DATE) AS parsed_date,
        CAST(value_mean AS DOUBLE) AS value_mean,
        CAST(value_min  AS DOUBLE) AS value_min,
        CAST(value_max  AS DOUBLE) AS value_max,
        CAST(value_sum  AS DOUBLE) AS value_sum,
        CAST(n_obs AS INTEGER) AS n_obs
    FROM "panama-canal-authority-values"
)
SELECT
    series_id,
    parameter,
    label,
    location_identifier,
    watershed,
    unit,
    parsed_date AS date,
    value_mean,
    value_min,
    value_max,
    value_sum,
    n_obs
FROM parsed
WHERE parsed_date IS NOT NULL
  AND value_mean IS NOT NULL AND isfinite(value_mean)
  -- Drop sentinel/placeholder timestamps: a stray 1900-01-01 null-date
  -- marker and any future-dated rows (forecast stragglers — no real
  -- observation lies in the future). Genuine historical data (1930s+)
  -- is kept.
  AND parsed_date > DATE '1900-01-01'
  AND parsed_date <= current_date
