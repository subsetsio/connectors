-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "unit",
    "schedule",
    "tra_cov",
    "tra_meas",
    "geo",
    strptime("time_period", '%Y-%m')::DATE AS time_period,
    "value",
    "flag"
FROM "eurostat-ttr00016"
