-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "energy_products",
    "distillate_type",
    "value_ktoe"
FROM "sg-data-d-60634abbf4b55bf18355c30c07b7037f"
