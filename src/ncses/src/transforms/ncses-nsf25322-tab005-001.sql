-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Age sex ethnicity race disability status and age at onset of disability" AS age_sex_ethnicity_race_disability_status_and_age_at_onset_of_disability,
    "Total" AS total,
    "Employed in all occupations - Employed" AS employed_in_all_occupations_employed,
    "Employed in all occupations - Full time" AS employed_in_all_occupations_full_time,
    "Employed in all occupations - Part time" AS employed_in_all_occupations_part_time,
    "Employed in S and E occupations - Full time" AS employed_in_s_and_e_occupations_full_time,
    "Employed in S and E occupations - Part time" AS employed_in_s_and_e_occupations_part_time,
    "Employed in S and E-related occupations - Full time" AS employed_in_s_and_e_related_occupations_full_time,
    "Employed in S and E-related occupations - Part time" AS employed_in_s_and_e_related_occupations_part_time,
    "Employed in non-S and E occupations - Full time" AS employed_in_non_s_and_e_occupations_full_time,
    "Employed in non-S and E occupations - Part time" AS employed_in_non_s_and_e_occupations_part_time,
    "Unemployeda - Part time" AS unemployeda_part_time,
    "Not in labor forceb - Total" AS not_in_labor_forceb_total,
    "Not in labor forceb - Student" AS not_in_labor_forceb_student,
    "Not in labor forceb - Retired" AS not_in_labor_forceb_retired,
    "Not in labor forceb - Not seeking employment all other reasons" AS not_in_labor_forceb_not_seeking_employment_all_other_reasons,
    "Full-time employed salary $ - Not seeking employment all other reasons" AS full_time_employed_salary_not_seeking_employment_all_other_reasons
FROM "ncses-nsf25322-tab005-001"
