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
    "breakdown_topic",
    "breakdown",
    "subject",
    "qualification_type",
    "qualification",
    "student_count",
    "student_pass_count",
    "student_pass_percent",
    "version"
FROM "dfe-019d9136-41d3-7160-8b01-7a4e59931a47"
