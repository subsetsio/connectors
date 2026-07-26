-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "_year" AS year,
    "total_enrollment_prek_to_12",
    "female",
    "male",
    "asian",
    "black",
    "hispanic",
    "multiple_race_categories_not_represented_other",
    "white",
    "students_with_disabilities",
    "english_language_learners",
    "poverty",
    "_039" AS 039,
    "_40_to_79" AS 40_to_79,
    "_80_or_greater" AS 80_or_greater
FROM "nyc-open-data-kiwq-bb5k"
