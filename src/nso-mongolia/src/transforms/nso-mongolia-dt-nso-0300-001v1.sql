-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicators" AS indicators,
    "Region" AS region,
    "Quarter" AS quarter,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0300-001v1"
