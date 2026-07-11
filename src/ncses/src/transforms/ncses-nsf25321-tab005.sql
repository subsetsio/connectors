-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study" AS field_of_study,
    "U.S. residing - All - Number" AS u_s_residing_all_number,
    "U.S. residing - All - SE" AS u_s_residing_all_se,
    "U.S. residing - Male - Number" AS u_s_residing_male_number,
    "U.S. residing - Male - SE" AS u_s_residing_male_se,
    "U.S. residing - Female - Number" AS u_s_residing_female_number,
    "U.S. residing - Female - SE" AS u_s_residing_female_se,
    "Non-U.S. residing - All - Number" AS non_u_s_residing_all_number,
    "Non-U.S. residing - All - SE" AS non_u_s_residing_all_se,
    "Non-U.S. residing - Male - Number" AS non_u_s_residing_male_number,
    "Non-U.S. residing - Male - SE" AS non_u_s_residing_male_se,
    "Non-U.S. residing - Female - Number" AS non_u_s_residing_female_number,
    "Non-U.S. residing - Female - SE" AS non_u_s_residing_female_se
FROM "ncses-nsf25321-tab005"
