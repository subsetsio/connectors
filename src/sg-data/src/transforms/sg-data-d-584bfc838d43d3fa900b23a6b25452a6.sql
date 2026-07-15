-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "gender",
    "number_of_donors"
FROM "sg-data-d-584bfc838d43d3fa900b23a6b25452a6"
