-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_interest_groups",
    "no_of_interest_groups"
FROM "sg-data-d-99e4b640badd48ab624eb6bffe2a9f0e"
