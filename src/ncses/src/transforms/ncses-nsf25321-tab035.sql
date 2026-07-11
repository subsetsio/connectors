-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation" AS occupation,
    "Total - Number" AS total_number,
    "Total - SE" AS total_se,
    "With disability - Number" AS with_disability_number,
    "With disability - SE" AS with_disability_se,
    "Without disability - Number" AS without_disability_number,
    "Without disability - SE" AS without_disability_se
FROM "ncses-nsf25321-tab035"
