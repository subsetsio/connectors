-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study" AS field_of_study,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "Educational institutiona - Number" AS educational_institutiona_number,
    "Educational institutiona - SE" AS educational_institutiona_se,
    "Business or industryb - Number" AS business_or_industryb_number,
    "Business or industryb - SE" AS business_or_industryb_se,
    "Governmentc - Number" AS governmentc_number,
    "Governmentc - SE" AS governmentc_se
FROM "ncses-nsf25321-tab012-003"
