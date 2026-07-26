-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "school_type",
    "overall_score",
    "overall_grade",
    "percentile_rank",
    "progress_grade",
    "performance_grade",
    "environment_grade",
    "college_and_career_readiness_grade",
    "closing_the_achievement_gap_points",
    "principal",
    "enrollment",
    "average_english_proficiency",
    "average_math_proficiency",
    "students_with_disabilities",
    "selfcontained",
    "overage",
    "black_or_hispanic",
    "ell"
FROM "nyc-open-data-dw8c-pxy2"
