-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; treat rows as source observations at the published granularity.
SELECT
    "date",
    "unemployed_15_24",
    "u_rate_15_24",
    "unemployed_15_30",
    "u_rate_15_30"
FROM "dosm-lfs-month-youth"
