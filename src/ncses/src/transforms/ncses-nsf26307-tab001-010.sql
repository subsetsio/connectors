-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "All full-time graduate students - Total" AS all_full_time_graduate_students_total,
    "All full-time graduate students - First time - Number" AS all_full_time_graduate_students_first_time_number,
    "All full-time graduate students - First time - Percent" AS all_full_time_graduate_students_first_time_percent,
    "Full-time master's students - Total - Percent" AS full_time_master_s_students_total_percent,
    "Full-time master's students - First time - Number" AS full_time_master_s_students_first_time_number,
    "Full-time master's students - First time - Percent" AS full_time_master_s_students_first_time_percent,
    "Full-time doctoral students - Total - Percent" AS full_time_doctoral_students_total_percent,
    "Full-time doctoral students - First time - Number" AS full_time_doctoral_students_first_time_number,
    "Full-time doctoral students - First time - Percent" AS full_time_doctoral_students_first_time_percent
FROM "ncses-nsf26307-tab001-010"
