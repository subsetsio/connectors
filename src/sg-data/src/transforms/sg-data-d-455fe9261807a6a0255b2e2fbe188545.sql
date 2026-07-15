-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "patents_applied",
    "patents_awarded",
    "patents_owned"
FROM "sg-data-d-455fe9261807a6a0255b2e2fbe188545"
