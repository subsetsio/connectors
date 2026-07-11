-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study and sex" AS field_of_study_and_sex,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "Full professor - Number" AS full_professor_number,
    "Full professor - SE" AS full_professor_se,
    "Associate professor - Number" AS associate_professor_number,
    "Associate professor - SE" AS associate_professor_se,
    "Assistant professor - Number" AS assistant_professor_number,
    "Assistant professor - SE" AS assistant_professor_se,
    "Instructor or lecturer - Number" AS instructor_or_lecturer_number,
    "Instructor or lecturer - SE" AS instructor_or_lecturer_se,
    "All other faculty - Number" AS all_other_faculty_number,
    "All other faculty - SE" AS all_other_faculty_se,
    "Rank not applicable - Number" AS rank_not_applicable_number,
    "Rank not applicable - SE" AS rank_not_applicable_se
FROM "ncses-nsf25321-tab017"
