-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are daily aggregates across heterogeneous hydrology, meteorology, and oceanography parameters; filter by parameter and unit before comparing or aggregating values.
SELECT
    "series_id",
    "parameter",
    "label",
    "location_identifier",
    "watershed",
    "unit",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "value_mean",
    "value_min",
    "value_max",
    "value_sum",
    "n_obs"
FROM "panama-canal-authority-values"
