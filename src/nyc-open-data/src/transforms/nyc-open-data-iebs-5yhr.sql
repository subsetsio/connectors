-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_category",
    "geographic_subdivision",
    "school_name",
    "grade",
    "_year" AS year,
    "student_category",
    "number_tested",
    "mean_scale_score",
    "num_level_1",
    "pct_level_1",
    "num_level_2",
    "pct_level_2",
    "num_level_3",
    "pct_level_3",
    "num_level_4",
    "pct_level_4",
    "num_level_3_and_4",
    "pct_level_3_and_4"
FROM "nyc-open-data-iebs-5yhr"
