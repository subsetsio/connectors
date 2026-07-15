-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "status",
    "sex",
    "no_of_drug_abusers"
FROM "sg-data-d-44c6b6dabcde1025724cab86b7d1672e"
