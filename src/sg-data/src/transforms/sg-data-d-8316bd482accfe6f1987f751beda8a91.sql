-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "scholarship_and_awards",
    "description",
    "reference"
FROM "sg-data-d-8316bd482accfe6f1987f751beda8a91"
