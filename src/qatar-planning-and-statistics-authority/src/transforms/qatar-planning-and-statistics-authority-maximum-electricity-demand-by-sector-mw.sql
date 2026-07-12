-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "system_maximum_demand",
    "industrial_maximum_demand",
    "domestic_maximum_demand"
FROM "qatar-planning-and-statistics-authority-maximum-electricity-demand-by-sector-mw"
