-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Sex citizenship ethnicity and race" AS sex_citizenship_ethnicity_and_race,
    "Full time - All full time - Total - Number" AS full_time_all_full_time_total_number,
    "Full time - All full time - Total - Percent" AS full_time_all_full_time_total_percent,
    "Full time - All full time - Master's - Number" AS full_time_all_full_time_master_s_number,
    "Full time - All full time - Master's - Percent" AS full_time_all_full_time_master_s_percent,
    "Full time - All full time - Doctoral - Number" AS full_time_all_full_time_doctoral_number,
    "Full time - All full time - Doctoral - Percent" AS full_time_all_full_time_doctoral_percent,
    "Full time - First time full time - All first time full time - Number" AS full_time_first_time_full_time_all_first_time_full_time_number,
    "Full time - First time full time - All first time full time - Percent" AS full_time_first_time_full_time_all_first_time_full_time_percent,
    "Full time - First time full time - Master's - Number" AS full_time_first_time_full_time_master_s_number,
    "Full time - First time full time - Master's - Percent" AS full_time_first_time_full_time_master_s_percent,
    "Full time - First time full time - Doctoral - Number" AS full_time_first_time_full_time_doctoral_number,
    "Full time - First time full time - Doctoral - Percent" AS full_time_first_time_full_time_doctoral_percent,
    "Part time - First time full time - All part time - Number" AS part_time_first_time_full_time_all_part_time_number,
    "Part time - First time full time - All part time - Percent" AS part_time_first_time_full_time_all_part_time_percent,
    "Part time - First time full time - Master's - Number" AS part_time_first_time_full_time_master_s_number,
    "Part time - First time full time - Master's - Percent" AS part_time_first_time_full_time_master_s_percent,
    "Part time - First time full time - Doctoral - Number" AS part_time_first_time_full_time_doctoral_number,
    "Part time - First time full time - Doctoral - Percent" AS part_time_first_time_full_time_doctoral_percent
FROM "ncses-nsf26307-tab002-008"
