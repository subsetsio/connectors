-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "tra_meas",
    "unit",
    "airp_pr",
    "time_period",
    "value",
    "flag"
FROM "eurostat-avia-gor-rs"
