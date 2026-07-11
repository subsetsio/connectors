-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Fiscal year" AS fiscal_year,
    "Total" AS total,
    "Total R and D" AS total_r_and_d,
    "Total research" AS total_research,
    "Basic research" AS basic_research,
    "Applied research" AS applied_research,
    "Development" AS development,
    "R and D plant" AS r_and_d_plant
FROM "ncses-nsf21329-tab001"
