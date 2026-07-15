-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "institution_type",
    "sector",
    "no_of_facilities"
FROM "sg-data-d-d4386b3130f3e5f7ccbbfc785602a606"
