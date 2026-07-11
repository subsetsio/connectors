-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study" AS field_of_study,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "Under 35 - Number" AS under_35_number,
    "Under 35 - SE" AS under_35_se,
    "35–39 - Number" AS 35_39_number,
    "35–39 - SE" AS 35_39_se,
    "40–44 - Number" AS 40_44_number,
    "40–44 - SE" AS 40_44_se,
    "45–49 - Number" AS 45_49_number,
    "45–49 - SE" AS 45_49_se,
    "50–54 - Number" AS 50_54_number,
    "50–54 - SE" AS 50_54_se,
    "55–59 - Number" AS 55_59_number,
    "55–59 - SE" AS 55_59_se,
    "60–64 - Number" AS 60_64_number,
    "60–64 - SE" AS 60_64_se,
    "65–75 - Number" AS 65_75_number,
    "65–75 - SE" AS 65_75_se
FROM "ncses-nsf25321-tab010"
