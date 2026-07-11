-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Economic activity" AS economic_activity,
    "Region" AS region,
    "Quarter" AS quarter,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-2600-017v1"
