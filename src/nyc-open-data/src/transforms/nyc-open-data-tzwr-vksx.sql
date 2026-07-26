-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "borough",
    "small_ps_bldgs",
    "small_ps_seats",
    "small_ps_cost",
    "psis_bldgs",
    "psis_seats",
    "psis_cost",
    "ishs_bldgs",
    "ishs_seats",
    "ishs_cost"
FROM "nyc-open-data-tzwr-vksx"
