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
    "rank",
    "progress_grade",
    "performance_grade",
    "environment_grade",
    "closing_the_achievement_gap_points",
    "principal",
    "enrollment"
FROM "nyc-open-data-gdpi-hegk"
