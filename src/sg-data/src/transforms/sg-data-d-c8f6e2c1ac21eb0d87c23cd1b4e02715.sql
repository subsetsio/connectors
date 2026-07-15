-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period_starting",
    "period_ending",
    "site",
    "gender",
    "asir"
FROM "sg-data-d-c8f6e2c1ac21eb0d87c23cd1b4e02715"
