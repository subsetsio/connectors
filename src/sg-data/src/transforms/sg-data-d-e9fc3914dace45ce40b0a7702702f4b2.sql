-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "employment_status",
    "highest_qualification_attained",
    "employed"
FROM "sg-data-d-e9fc3914dace45ce40b0a7702702f4b2"
