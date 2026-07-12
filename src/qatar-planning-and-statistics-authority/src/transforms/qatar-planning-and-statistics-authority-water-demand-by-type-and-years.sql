-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "average_distribution_demand_migd",
    "average_industrial_demand_migd",
    "average_domestic_demand_migd"
FROM "qatar-planning-and-statistics-authority-water-demand-by-type-and-years"
