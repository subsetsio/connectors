-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_grp",
    "no_of_active_mbrs"
FROM "sg-data-d-6ade0eac937ce9f8b6707905dfdf1ddd"
