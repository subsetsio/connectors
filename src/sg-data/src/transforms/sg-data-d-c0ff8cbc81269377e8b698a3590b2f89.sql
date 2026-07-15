-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "institution_type",
    "facility_type_b",
    "no_of_visits"
FROM "sg-data-d-c0ff8cbc81269377e8b698a3590b2f89"
