-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "age_group",
    "knowledge_on_wholegrain",
    "aware_of_transfat"
FROM "sg-data-d-4b983af77d4ae25b505d84570794139d"
