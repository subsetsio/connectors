-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "institution_type",
    "facility_type_a",
    "public_private",
    "no_of_facilities",
    "no_beds"
FROM "sg-data-d-852ebeb1165d0ec4cdc89fa7742959d1"
