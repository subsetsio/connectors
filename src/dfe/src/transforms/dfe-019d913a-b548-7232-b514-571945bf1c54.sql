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
    "cohort",
    "breakdown_topic",
    "breakdown",
    "ofqual_tier_1",
    "ofqual_tier_2",
    "student_count",
    "student_pass_count",
    "student_pass_percent",
    "version"
FROM "dfe-019d913a-b548-7232-b514-571945bf1c54"
