-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study and sex" AS field_of_study_and_sex,
    "All employed - < 10 - Number" AS all_employed_10_number,
    "All employed - < 10 - SE" AS all_employed_10_se,
    "All employed - ≥ 10 - Number" AS all_employed_10_number_2,
    "All employed - ≥ 10 - SE" AS all_employed_10_se_2,
    "Full professor - < 10 - Number" AS full_professor_10_number,
    "Full professor - < 10 - SE" AS full_professor_10_se,
    "Full professor - ≥ 10 - Number" AS full_professor_10_number_2,
    "Full professor - ≥ 10 - SE" AS full_professor_10_se_2,
    "Associate professor - < 10 - Number" AS associate_professor_10_number,
    "Associate professor - < 10 - SE" AS associate_professor_10_se,
    "Associate professor - ≥ 10 - Number" AS associate_professor_10_number_2,
    "Associate professor - ≥ 10 - SE" AS associate_professor_10_se_2,
    "Assistant professor - < 10 - Number" AS assistant_professor_10_number,
    "Assistant professor - < 10 - SE" AS assistant_professor_10_se,
    "Assistant professor - ≥ 10 - Number" AS assistant_professor_10_number_2,
    "Assistant professor - ≥ 10 - SE" AS assistant_professor_10_se_2,
    "Instructor or lecturer - < 10 - Number" AS instructor_or_lecturer_10_number,
    "Instructor or lecturer - < 10 - SE" AS instructor_or_lecturer_10_se,
    "Instructor or lecturer - ≥ 10 - Number" AS instructor_or_lecturer_10_number_2,
    "Instructor or lecturer - ≥ 10 - SE" AS instructor_or_lecturer_10_se_2,
    "All other faculty - < 10 - Number" AS all_other_faculty_10_number,
    "All other faculty - < 10 - SE" AS all_other_faculty_10_se,
    "All other faculty - ≥ 10 - Number" AS all_other_faculty_10_number_2,
    "All other faculty - ≥ 10 - SE" AS all_other_faculty_10_se_2,
    "Rank not applicable - < 10 - Number" AS rank_not_applicable_10_number,
    "Rank not applicable - < 10 - SE" AS rank_not_applicable_10_se,
    "Rank not applicable - ≥ 10 - Number" AS rank_not_applicable_10_number_2,
    "Rank not applicable - ≥ 10 - SE" AS rank_not_applicable_10_se_2
FROM "ncses-nsf25321-tab018"
