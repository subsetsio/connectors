-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "age_group",
    "number_of_donors"
FROM "sg-data-d-5901cb0815687f7e31ca626878ee09a7"
