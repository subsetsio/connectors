-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "hiv_aids_knowledge",
    "proportion"
FROM "sg-data-d-eb4be8c8e136b255a7b6a4e7d5e73964"
