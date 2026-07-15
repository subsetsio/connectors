-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "rh_mean_daily",
    "rh_mean_daily_minimum",
    "rh_means_daily_maximum"
FROM "sg-data-d-31dbf162e94f76065e1e4c60a80a4264"
