SELECT
    series_code,
    obs_date,
    value
FROM (
    SELECT
        series_code,
        obs_date,
        TRY_CAST(value AS DOUBLE) AS value,
        row_number() OVER (
            PARTITION BY series_code, obs_date
            ORDER BY value DESC
        ) AS _rn
    FROM "bank-of-england-values"
    WHERE series_code IS NOT NULL
      AND obs_date IS NOT NULL
)
WHERE _rn = 1
  AND value IS NOT NULL
