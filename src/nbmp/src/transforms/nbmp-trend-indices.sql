SELECT
    geographical_scale,
    species,
    survey,
    official_statistic,
    CAST(TRY_CAST(year AS DOUBLE) AS INTEGER) AS year,
    TRY_CAST(smoothed_index AS DOUBLE)        AS smoothed_index,
    TRY_CAST(se AS DOUBLE)                    AS standard_error,
    TRY_CAST(lower_95_ci AS DOUBLE)           AS lower_95_ci,
    TRY_CAST(upper_95_ci AS DOUBLE)           AS upper_95_ci
FROM "nbmp-trend-indices"
WHERE TRY_CAST(year AS INTEGER) IS NOT NULL
  AND TRY_CAST(smoothed_index AS DOUBLE) IS NOT NULL
  AND species IS NOT NULL
