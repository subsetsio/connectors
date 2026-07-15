-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "ethnic_group",
    "flat_type",
    "percentage"
FROM "sg-data-d-6f0b9b4e1a64a09f5b76c8a2c1234d2d"
