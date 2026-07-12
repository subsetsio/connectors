-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "average_distribution_demand_migd",
    "growth",
    "maximum_demand_migd",
    "maximum_demand_month",
    "shhr_l_qs",
    "minimum_demand_migd",
    "minimum_demand_month",
    "shhr_l_dn"
FROM "qatar-planning-and-statistics-authority-water-distribution-maximum-and-minimum-demand-by-year"
