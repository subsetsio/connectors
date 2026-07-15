-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "energy_products",
    "sub_products",
    "value_ktoe"
FROM "sg-data-d-3ab96fa71a5ba50cd06f06fc0fadc9fd"
