-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study and sex" AS field_of_study_and_sex,
    "All full-time employed - Median salary" AS all_full_time_employed_median_salary,
    "All full-time employed - SE" AS all_full_time_employed_se,
    "Full professor - Median salary" AS full_professor_median_salary,
    "Full professor - SE" AS full_professor_se,
    "Associate professor - Median salary" AS associate_professor_median_salary,
    "Associate professor - SE" AS associate_professor_se,
    "Assistant professor - Median salary" AS assistant_professor_median_salary,
    "Assistant professor - SE" AS assistant_professor_se,
    "Instructor or lecturer - Median salary" AS instructor_or_lecturer_median_salary,
    "Instructor or lecturer - SE" AS instructor_or_lecturer_se,
    "All other faculty - Median salary" AS all_other_faculty_median_salary,
    "All other faculty - SE" AS all_other_faculty_se,
    "Rank not applicable - Median salary" AS rank_not_applicable_median_salary,
    "Rank not applicable - SE" AS rank_not_applicable_se
FROM "ncses-nsf25321-tab059"
