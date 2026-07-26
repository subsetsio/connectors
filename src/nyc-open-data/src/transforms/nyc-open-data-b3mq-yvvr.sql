-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "facility",
    "_year" AS year,
    "_month" AS month,
    "sludge_digested_wet_tons",
    "food_scraps_digested_wet_tons",
    "rng_production_mmbtu",
    "rng_system_uptime",
    "flared_biogas_mscf",
    "reduction_in_flaring"
FROM "nyc-open-data-b3mq-yvvr"
