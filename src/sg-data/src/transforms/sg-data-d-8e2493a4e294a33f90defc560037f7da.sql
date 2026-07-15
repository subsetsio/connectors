-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "energy_products",
    "sub_products",
    "value_ktoe"
FROM "sg-data-d-8e2493a4e294a33f90defc560037f7da"
