-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Occupation" AS occupation,
    "All employed - Total - Number" AS all_employed_total_number,
    "All employed - Total - SE" AS all_employed_total_se,
    "All employed - Male - Number" AS all_employed_male_number,
    "All employed - Male - SE" AS all_employed_male_se,
    "All employed - Female - Number" AS all_employed_female_number,
    "All employed - Female - SE" AS all_employed_female_se,
    "Asiana - Total - Number" AS asiana_total_number,
    "Asiana - Total - SE" AS asiana_total_se,
    "Asiana - Male - Number" AS asiana_male_number,
    "Asiana - Male - SE" AS asiana_male_se,
    "Asiana - Female - Number" AS asiana_female_number,
    "Asiana - Female - SE" AS asiana_female_se,
    "Other minorityb - Total - Number" AS other_minorityb_total_number,
    "Other minorityb - Total - SE" AS other_minorityb_total_se,
    "Other minorityb - Male - Number" AS other_minorityb_male_number,
    "Other minorityb - Male - SE" AS other_minorityb_male_se,
    "Other minorityb - Female - Number" AS other_minorityb_female_number,
    "Other minorityb - Female - SE" AS other_minorityb_female_se,
    "Whitec - Total - Number" AS whitec_total_number,
    "Whitec - Total - SE" AS whitec_total_se,
    "Whitec - Male - Number" AS whitec_male_number,
    "Whitec - Male - SE" AS whitec_male_se,
    "Whitec - Female - Number" AS whitec_female_number,
    "Whitec - Female - SE" AS whitec_female_se
FROM "ncses-nsf25321-tab037"
