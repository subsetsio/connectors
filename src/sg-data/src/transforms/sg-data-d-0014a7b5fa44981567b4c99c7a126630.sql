-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "qtr",
    "no_of_mbrs"
FROM "sg-data-d-0014a7b5fa44981567b4c99c7a126630"
