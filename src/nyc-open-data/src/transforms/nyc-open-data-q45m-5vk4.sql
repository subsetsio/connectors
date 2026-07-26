-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "_year" AS year,
    "total_enrollment",
    "female",
    "male",
    "asian",
    "black",
    "hispanic",
    "multiple_race_categories_not_represented",
    "white",
    "students_with_disabilities",
    "english_language_learners",
    "poverty",
    "iep_recommended_portion_of_school_day_in_general_ed_039",
    "iep_recommended_portion_of_school_day_in_general_ed_4079",
    "iep_recommended_portion_of_school_day_in_general_ed_80_or_greater"
FROM "nyc-open-data-q45m-5vk4"
