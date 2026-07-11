-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are daily aggregates across heterogeneous hydrology, meteorology, and oceanography parameters; filter by parameter and unit before comparing or aggregating values.
WITH parsed AS (
    SELECT
        "series_id",
        "parameter",
        "label",
        "location_identifier",
        "watershed",
        "unit",
        TRY_CAST("date" AS DATE) AS parsed_date,
        "value_mean",
        "value_min",
        "value_max",
        "value_sum",
        "n_obs"
    FROM "panama-canal-authority-values"
)
SELECT
    "series_id",
    "parameter",
    "label",
    "location_identifier",
    "watershed",
    "unit",
    parsed_date AS date,
    "value_mean",
    "value_min",
    "value_max",
    "value_sum",
    "n_obs"
FROM parsed
WHERE parsed_date IS NOT NULL
  AND "value_mean" IS NOT NULL AND isfinite("value_mean")
  -- Drop placeholder and future rows without removing valid historical data.
  AND parsed_date > DATE '1900-01-01'
  AND parsed_date <= current_date
