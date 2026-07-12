-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "company",
    "lshrk",
    "independent_power_water_producer",
    "lmntj",
    "contracted_capacity_mw"
FROM "qatar-planning-and-statistics-authority-contracted-capacities-by-iwpps"
