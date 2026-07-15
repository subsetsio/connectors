-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "rail_type",
    "length"
FROM "sg-data-d-d6e505b87580a4bae4aae0beb07d3de6"
