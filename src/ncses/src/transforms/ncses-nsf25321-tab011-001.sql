-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study" AS field_of_study,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "≤ 5 - Number" AS 5_number,
    "≤ 5 - SE" AS 5_se,
    "6–10 - Number" AS 6_10_number,
    "6–10 - SE" AS 6_10_se,
    "11–15 - Number" AS 11_15_number,
    "11–15 - SE" AS 11_15_se,
    "16–20 - Number" AS 16_20_number,
    "16–20 - SE" AS 16_20_se,
    "21–25 - Number" AS 21_25_number,
    "21–25 - SE" AS 21_25_se,
    "> 25 - Number" AS 25_number,
    "> 25 - SE" AS 25_se
FROM "ncses-nsf25321-tab011-001"
