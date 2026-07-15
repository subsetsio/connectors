-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "status",
    "ethnic_group",
    "no_of_drug_abusers"
FROM "sg-data-d-0e3352ebb178b555f5bd0ed97c20dd8c"
