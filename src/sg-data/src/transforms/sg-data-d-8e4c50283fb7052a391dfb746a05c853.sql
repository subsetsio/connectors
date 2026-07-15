-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "property_type",
    "locality",
    "index"
FROM "sg-data-d-8e4c50283fb7052a391dfb746a05c853"
