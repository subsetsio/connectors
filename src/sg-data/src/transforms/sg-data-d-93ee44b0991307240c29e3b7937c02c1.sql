-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "area",
    "domestic_exports"
FROM "sg-data-d-93ee44b0991307240c29e3b7937c02c1"
