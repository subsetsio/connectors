-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mother_nationality",
    "father_nationality",
    "birth_count"
FROM "sg-data-d-a4738ec298639102f2e9cc17afd5af7c"
