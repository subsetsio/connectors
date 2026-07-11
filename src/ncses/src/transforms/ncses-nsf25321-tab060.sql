-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study and sex" AS field_of_study_and_sex,
    "All full-time employed - < 10 - Median salary" AS all_full_time_employed_10_median_salary,
    "All full-time employed - < 10 - SE" AS all_full_time_employed_10_se,
    "All full-time employed - ≥ 10 - Median salary" AS all_full_time_employed_10_median_salary_2,
    "All full-time employed - ≥ 10 - SE" AS all_full_time_employed_10_se_2,
    "Full professor - < 10 - Median salary" AS full_professor_10_median_salary,
    "Full professor - < 10 - SE" AS full_professor_10_se,
    "Full professor - ≥ 10 - Median salary" AS full_professor_10_median_salary_2,
    "Full professor - ≥ 10 - SE" AS full_professor_10_se_2,
    "Associate professor - < 10 - Median salary" AS associate_professor_10_median_salary,
    "Associate professor - < 10 - SE" AS associate_professor_10_se,
    "Associate professor - ≥ 10 - Median salary" AS associate_professor_10_median_salary_2,
    "Associate professor - ≥ 10 - SE" AS associate_professor_10_se_2,
    "Assistant professor - < 10 - Median salary" AS assistant_professor_10_median_salary,
    "Assistant professor - < 10 - SE" AS assistant_professor_10_se,
    "Assistant professor - ≥ 10 - Median salary" AS assistant_professor_10_median_salary_2,
    "Assistant professor - ≥ 10 - SE" AS assistant_professor_10_se_2,
    "Instructor or lecturer - < 10 - Median salary" AS instructor_or_lecturer_10_median_salary,
    "Instructor or lecturer - < 10 - SE" AS instructor_or_lecturer_10_se,
    "Instructor or lecturer - ≥ 10 - Median salary" AS instructor_or_lecturer_10_median_salary_2,
    "Instructor or lecturer - ≥ 10 - SE" AS instructor_or_lecturer_10_se_2,
    "All other faculty - < 10 - Median salary" AS all_other_faculty_10_median_salary,
    "All other faculty - < 10 - SE" AS all_other_faculty_10_se,
    "All other faculty - ≥ 10 - Median salary" AS all_other_faculty_10_median_salary_2,
    "All other faculty - ≥ 10 - SE" AS all_other_faculty_10_se_2,
    "Rank not applicable - < 10 - Median salary" AS rank_not_applicable_10_median_salary,
    "Rank not applicable - < 10 - SE" AS rank_not_applicable_10_se,
    "Rank not applicable - ≥ 10 - Median salary" AS rank_not_applicable_10_median_salary_2,
    "Rank not applicable - ≥ 10 - SE" AS rank_not_applicable_10_se_2
FROM "ncses-nsf25321-tab060"
