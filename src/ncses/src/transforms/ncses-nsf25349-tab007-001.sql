-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "Doctorate-granting institutions number" AS doctorate_granting_institutions_number,
    "Doctorate recipients - Total number" AS doctorate_recipients_total_number,
    "Doctorate recipients - Mean per institution" AS doctorate_recipients_mean_per_institution,
    "Doctorate recipients - Median per institution" AS doctorate_recipients_median_per_institution
FROM "ncses-nsf25349-tab007-001"
