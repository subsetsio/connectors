-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All computer and information sciences fields" AS all_computer_and_information_sciences_fields,
    "Computer science" AS computer_science,
    "Computer and information sciences other" AS computer_and_information_sciences_other
FROM "ncses-nsf25349-tab008-005"
