-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; treat rows as source observations at the published granularity.
SELECT
    "date",
    "unemployed",
    "unemployed_active",
    "unemployed_active_3mo",
    "unemployed_active_6mo",
    "unemployed_active_12mo",
    "unemployed_active_long",
    "unemployed_inactive"
FROM "dosm-lfs-month-duration"
