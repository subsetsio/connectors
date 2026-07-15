-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "HALE_total_population_GBD" AS hale_total_population_gbd
FROM "sg-data-d-c93fe829a88716926223b5ad472e6044"
