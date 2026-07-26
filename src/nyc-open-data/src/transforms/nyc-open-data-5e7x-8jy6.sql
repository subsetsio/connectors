-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "total_parent_response_rate",
    "total_teacher_response_rate",
    "total_student_response_rate",
    "collaborative_teachers_score",
    "effective_school_leadership_score",
    "rigorous_instruction_score",
    "supportive_environment_score",
    "strong_familycommunity_ties_score",
    "trust_score"
FROM "nyc-open-data-5e7x-8jy6"
