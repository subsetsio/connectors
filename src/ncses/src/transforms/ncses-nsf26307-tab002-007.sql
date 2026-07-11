-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Detailed field" AS detailed_field,
    "All graduate students - Total - Number" AS all_graduate_students_total_number,
    "All graduate students - Total - Percent" AS all_graduate_students_total_percent,
    "All graduate students - Full time - All full time - Number" AS all_graduate_students_full_time_all_full_time_number,
    "All graduate students - Full time - All full time - Percent" AS all_graduate_students_full_time_all_full_time_percent,
    "All graduate students - Full time - First time full time - Number" AS all_graduate_students_full_time_first_time_full_time_number,
    "All graduate students - Full time - First time full time - Percent" AS all_graduate_students_full_time_first_time_full_time_percent,
    "All graduate students - Part time - First time full time - Number" AS all_graduate_students_part_time_first_time_full_time_number,
    "All graduate students - Part time - First time full time - Percent" AS all_graduate_students_part_time_first_time_full_time_percent,
    "Master's students - Total - First time full time - Number" AS master_s_students_total_first_time_full_time_number,
    "Master's students - Total - First time full time - Percent" AS master_s_students_total_first_time_full_time_percent,
    "Master's students - Full time - All full time - Number" AS master_s_students_full_time_all_full_time_number,
    "Master's students - Full time - All full time - Percent" AS master_s_students_full_time_all_full_time_percent,
    "Master's students - Full time - First time full time - Number" AS master_s_students_full_time_first_time_full_time_number,
    "Master's students - Full time - First time full time - Percent" AS master_s_students_full_time_first_time_full_time_percent,
    "Master's students - Part time - First time full time - Number" AS master_s_students_part_time_first_time_full_time_number,
    "Master's students - Part time - First time full time - Percent" AS master_s_students_part_time_first_time_full_time_percent,
    "Doctoral students - Total - First time full time - Number" AS doctoral_students_total_first_time_full_time_number,
    "Doctoral students - Total - First time full time - Percent" AS doctoral_students_total_first_time_full_time_percent,
    "Doctoral students - Full time - All full time - Number" AS doctoral_students_full_time_all_full_time_number,
    "Doctoral students - Full time - All full time - Percent" AS doctoral_students_full_time_all_full_time_percent,
    "Doctoral students - Full time - First time full time - Number" AS doctoral_students_full_time_first_time_full_time_number,
    "Doctoral students - Full time - First time full time - Percent" AS doctoral_students_full_time_first_time_full_time_percent,
    "Doctoral students - Part time - First time full time - Number" AS doctoral_students_part_time_first_time_full_time_number,
    "Doctoral students - Part time - First time full time - Percent" AS doctoral_students_part_time_first_time_full_time_percent
FROM "ncses-nsf26307-tab002-007"
