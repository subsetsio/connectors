-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "release",
    "dataset_id",
    "series_name",
    CAST("freq_code" AS BIGINT) AS freq_code,
    "frequency",
    "unit",
    CAST("unit_mult" AS BIGINT) AS unit_mult,
    "currency",
    "short_description",
    "long_description",
    "series_attributes",
    strptime("time_period", '%Y-%m-%d')::DATE AS time_period,
    "obs_value",
    "obs_status"
FROM "federal-reserve-z1"
