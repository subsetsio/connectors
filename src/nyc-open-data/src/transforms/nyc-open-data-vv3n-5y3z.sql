-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "overall_score",
    "overall_grade",
    "overall_rank",
    "progress_grade",
    "performance_grade",
    "environment_grade",
    "college_and_career_readiness_grade",
    "closing_the_achievement_gap_points",
    "assistant_principal",
    "enrollment",
    "school_type",
    "average_english_proficiency",
    "average_math_proficiency",
    "students_with_disabilities",
    "selfcontained",
    "overage",
    "black_or_hispanic",
    "ell"
FROM "nyc-open-data-vv3n-5y3z"
