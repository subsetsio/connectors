-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bn",
    "school_name",
    "progress_report_type",
    "_20122013_progress_report_grade" AS 20122013_progress_report_grade,
    "_20112012_progress_report_grade" AS 20112012_progress_report_grade,
    "_201011_progress_report_grade" AS 201011_progress_report_grade,
    "_200910_progress_report_grade" AS 200910_progress_report_grade,
    "_200809_progress_report_grade" AS 200809_progress_report_grade,
    "_200708_progress_report_grade" AS 200708_progress_report_grade,
    "_200607_progress_report_grade" AS 200607_progress_report_grade
FROM "nyc-open-data-4y63-yw9e"
