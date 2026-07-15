-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "admissions_by_education_level",
    "number_of_admissions"
FROM "sg-data-d-a166bc31ce8cb823b22467fb0798dff7"
