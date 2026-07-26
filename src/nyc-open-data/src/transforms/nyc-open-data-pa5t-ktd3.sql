-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "number_of_housing_units_20202024",
    "number_of_housing_units_20202029"
FROM "nyc-open-data-pa5t-ktd3"
