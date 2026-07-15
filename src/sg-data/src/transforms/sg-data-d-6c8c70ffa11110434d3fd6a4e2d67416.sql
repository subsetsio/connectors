-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs",
    "flat_type",
    "no_of_income_earners",
    "percentage"
FROM "sg-data-d-6c8c70ffa11110434d3fd6a4e2d67416"
