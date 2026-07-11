-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All psychology fields" AS all_psychology_fields,
    "Clinical psychology" AS clinical_psychology,
    "Counseling and applied psychology" AS counseling_and_applied_psychology,
    "Research and experimental psychology" AS research_and_experimental_psychology,
    "Psychology other" AS psychology_other
FROM "ncses-nsf25349-tab008-012"
