-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "end_of_day",
    "hkd_fer_spot",
    "hkd_fer_1w",
    "hkd_fer_1m",
    "hkd_fer_3m",
    "hkd_fer_6m",
    "hkd_fer_9m",
    "hkd_fer_12m"
FROM "hkma-hkd-forward-rates-daily"
