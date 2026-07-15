-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "facility_type_a",
    "sex",
    "rate"
FROM "sg-data-d-66c194105cb00ce79a024b0221ab055a"
