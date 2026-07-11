-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "Doctorate recipients number" AS doctorate_recipients_number,
    "% change from previous year" AS change_from_previous_year
FROM "ncses-nsf25349-tab001-001"
