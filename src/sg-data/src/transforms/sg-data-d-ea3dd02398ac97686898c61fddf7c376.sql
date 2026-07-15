-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_interest_groups",
    "no_of_members"
FROM "sg-data-d-ea3dd02398ac97686898c61fddf7c376"
