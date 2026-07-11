-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All geosciences atmospheric and ocean sciences fields" AS all_geosciences_atmospheric_and_ocean_sciences_fields,
    "Geological and earth sciences" AS geological_and_earth_sciences,
    "Ocean marine and atmospheric sciences" AS ocean_marine_and_atmospheric_sciences
FROM "ncses-nsf25349-tab008-007"
