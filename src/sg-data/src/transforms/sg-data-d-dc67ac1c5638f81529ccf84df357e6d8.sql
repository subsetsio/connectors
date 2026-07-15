-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_of_occurrence",
    "classification",
    "type_of_vessel",
    "description",
    "url"
FROM "sg-data-d-dc67ac1c5638f81529ccf84df357e6d8"
