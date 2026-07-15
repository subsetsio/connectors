-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "facility_type_a",
    "sex",
    "age",
    "rate"
FROM "sg-data-d-dd32a9abff167b63efc11fb2f25cb341"
