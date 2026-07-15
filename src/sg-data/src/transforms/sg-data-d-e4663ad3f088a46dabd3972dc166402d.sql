-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "institution_type",
    "sector",
    "facility_type_b",
    "no_of_facilities"
FROM "sg-data-d-e4663ad3f088a46dabd3972dc166402d"
