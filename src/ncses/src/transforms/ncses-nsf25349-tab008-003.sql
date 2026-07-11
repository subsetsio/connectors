-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All agricultural sciences and natural resources fields" AS all_agricultural_sciences_and_natural_resources_fields,
    "Agricultural animal plant and veterinary sciences" AS agricultural_animal_plant_and_veterinary_sciences,
    "Natural resources and conservation" AS natural_resources_and_conservation
FROM "ncses-nsf25349-tab008-003"
