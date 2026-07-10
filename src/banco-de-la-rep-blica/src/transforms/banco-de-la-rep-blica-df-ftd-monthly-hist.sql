-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_area",
    "subject",
    "expenditure",
    "activity",
    "adjustment",
    "unit_measure",
    "freq",
    "domain",
    CAST("unit_mult" AS BIGINT) AS unit_mult,
    strptime("time_period", '%Y-%m')::DATE AS time_period,
    CAST("obs_value" AS DOUBLE) AS obs_value,
    "obs_status"
FROM "banco-de-la-rep-blica-df-ftd-monthly-hist"
