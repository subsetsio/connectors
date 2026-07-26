-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "dbn",
    "school_name",
    "total_enrollment_pk12",
    "female",
    "male",
    "asian",
    "black",
    "hispanic",
    "other",
    "white",
    "students_with_disabilities",
    "english_language_learners",
    "eligible_for_free_or_reduced_lunches",
    "ict",
    "special_class",
    "setss"
FROM "nyc-open-data-5cd6-v74i"
