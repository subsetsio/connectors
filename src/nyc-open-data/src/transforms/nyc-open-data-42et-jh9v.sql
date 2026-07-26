-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "quality_review_year",
    "quality_review_score",
    "progress_rpt_1011",
    "student_progress_1011",
    "student_perf_1011",
    "envi_1011",
    "college_ready_1011",
    "graduation_201011",
    "college_enroll_201011",
    "progress_rpt_1112",
    "student_progress_1112",
    "student_perf_1112",
    "envi_1112",
    "college_ready_1112",
    "graduation_201112",
    "college_enroll_201112"
FROM "nyc-open-data-42et-jh9v"
