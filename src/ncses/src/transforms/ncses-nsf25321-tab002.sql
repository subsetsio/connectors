-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study and sex" AS field_of_study_and_sex,
    "Total - Number" AS total_number,
    "Total - SE" AS total_se,
    "Employed - Total - Number" AS employed_total_number,
    "Employed - Total - SE" AS employed_total_se,
    "Employed - Full time - Number" AS employed_full_time_number,
    "Employed - Full time - SE" AS employed_full_time_se,
    "Employed - Part time - Number" AS employed_part_time_number,
    "Employed - Part time - SE" AS employed_part_time_se,
    "Unemployeda - Part time - Number" AS unemployeda_part_time_number,
    "Unemployeda - Part time - SE" AS unemployeda_part_time_se,
    "Retired - Part time - Number" AS retired_part_time_number,
    "Retired - Part time - SE" AS retired_part_time_se,
    "Not employed and not seeking workb - Part time - Number" AS not_employed_and_not_seeking_workb_part_time_number,
    "Not employed and not seeking workb - Part time - SE" AS not_employed_and_not_seeking_workb_part_time_se
FROM "ncses-nsf25321-tab002"
