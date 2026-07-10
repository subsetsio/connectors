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
    "disadvantage_status",
    "exam_cohort",
    "qualification_level",
    "year_1_student_count",
    "year_2_student_count",
    "retained_student_count",
    "retained_assessed_student_count",
    "retained_2nd_year_student_count",
    "retained_percent",
    "retained_assessed_percent",
    "retained_2nd_year_percent"
FROM "dfe-019d913a-35c8-72d5-a240-9ab935f08b87"
