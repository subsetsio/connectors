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
    "exam_cohort",
    CAST("student_count" AS BIGINT) AS student_count,
    CAST("student_percent" AS DOUBLE) AS student_percent
FROM "dfe-019d9133-9db4-75b7-b6ed-9996c513f1b7"
