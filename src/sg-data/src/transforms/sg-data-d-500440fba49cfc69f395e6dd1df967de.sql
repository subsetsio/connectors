-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "energy_products",
    "consumption_ktoe"
FROM "sg-data-d-500440fba49cfc69f395e6dd1df967de"
