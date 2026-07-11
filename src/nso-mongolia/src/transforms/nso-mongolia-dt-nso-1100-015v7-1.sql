-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicator" AS indicator,
    "Subdivision" AS subdivision,
    "Month" AS month,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-1100-015v7-1"
