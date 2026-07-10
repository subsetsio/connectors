-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "unemployed_15_24",
    "u_rate_15_24",
    "unemployed_15_30",
    "u_rate_15_30"
FROM "dosm-lfs-month-youth"
