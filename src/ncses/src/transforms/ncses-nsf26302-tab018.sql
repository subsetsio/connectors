-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "State and department or agency" AS state_and_department_or_agency,
    "All R and D expenditures" AS all_r_and_d_expenditures,
    "Source of funds - Federal government" AS source_of_funds_federal_government,
    "Source of funds - State and all othersa" AS source_of_funds_state_and_all_othersa
FROM "ncses-nsf26302-tab018"
