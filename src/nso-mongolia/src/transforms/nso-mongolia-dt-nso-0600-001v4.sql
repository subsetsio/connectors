-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Products" AS products,
    "Time" AS time,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0600-001v4"
