-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix geographical scales and survey methods; filter to one geography and survey before comparing species or interpreting a time series.
-- caution: Index values, standard errors, and confidence intervals are not additive across species, geographies, surveys, or years.
SELECT
    "geographical_scale",
    "species",
    "survey",
    "official_statistic",
    CAST("year" AS BIGINT) AS year,
    CAST("smoothed_index" AS DOUBLE) AS smoothed_index,
    CAST("se" AS DOUBLE) AS standard_error,
    CAST("lower_95_ci" AS DOUBLE) AS lower_95_ci,
    CAST("upper_95_ci" AS DOUBLE) AS upper_95_ci
FROM "nbmp-trend-indices"
