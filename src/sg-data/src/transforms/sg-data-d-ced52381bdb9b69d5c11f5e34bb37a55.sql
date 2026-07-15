-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "time_interval",
    "exclusive_breastfeeding",
    "any_breastfeeding"
FROM "sg-data-d-ced52381bdb9b69d5c11f5e34bb37a55"
