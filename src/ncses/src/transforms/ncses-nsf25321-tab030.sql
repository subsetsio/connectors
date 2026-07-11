-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation and employment status" AS occupation_and_employment_status,
    "Total - Number" AS total_number,
    "Total - SE" AS total_se,
    "Male - Number" AS male_number,
    "Male - SE" AS male_se,
    "Female - Number" AS female_number,
    "Female - SE" AS female_se
FROM "ncses-nsf25321-tab030"
