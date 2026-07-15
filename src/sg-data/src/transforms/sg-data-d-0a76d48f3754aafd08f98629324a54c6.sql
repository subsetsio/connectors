-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "bunker_type",
    "bunker_sales"
FROM "sg-data-d-0a76d48f3754aafd08f98629324a54c6"
