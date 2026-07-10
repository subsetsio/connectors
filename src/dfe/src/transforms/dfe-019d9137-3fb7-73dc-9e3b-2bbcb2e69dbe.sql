-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "version",
    "breakdown_topic",
    "breakdown",
    "subject_area",
    "subject",
    "exam_cohort",
    "grade",
    "grade_count",
    "grade_percent",
    "astar_to_grade_cumulative_count",
    "astar_to_grade_cumulative_percent"
FROM "dfe-019d9137-3fb7-73dc-9e3b-2bbcb2e69dbe"
