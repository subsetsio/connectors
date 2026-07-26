-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "total_enrollment_prek_to_12",
    "female",
    "male",
    "asian",
    "black",
    "hispanic",
    "other",
    "white",
    "students_with_disabilities",
    "english_language_learners",
    "poverty",
    "ict",
    "special_class",
    "setss"
FROM "nyc-open-data-iuvu-z276"
