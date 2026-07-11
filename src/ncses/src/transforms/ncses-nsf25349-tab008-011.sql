-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All physical sciences fields" AS all_physical_sciences_fields,
    "Astronomy and astrophysics" AS astronomy_and_astrophysics,
    "Chemistry" AS chemistry,
    "Materials sciences" AS materials_sciences,
    "Physics" AS physics
FROM "ncses-nsf25349-tab008-011"
