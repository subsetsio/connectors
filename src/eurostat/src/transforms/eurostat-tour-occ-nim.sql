-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "c_resid",
    "unit",
    "nace_r2",
    "geo",
    strptime("time_period", '%Y-%m')::DATE AS time_period,
    "value",
    "flag"
FROM "eurostat-tour-occ-nim"
