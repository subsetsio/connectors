-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "parent_company",
    "lshrk_l_m",
    "independent_power_water_producer",
    "mntj_ltq_wlmyh_lmstql",
    "contracted_capacity_water_migd",
    "mm3_day"
FROM "qatar-planning-and-statistics-authority-contracted-capacities-by-independent-power-and-water-producers-ipwp"
