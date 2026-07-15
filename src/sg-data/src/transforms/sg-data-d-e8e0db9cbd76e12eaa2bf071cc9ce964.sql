-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "LE_total_population_GBD" AS le_total_population_gbd
FROM "sg-data-d-e8e0db9cbd76e12eaa2bf071cc9ce964"
