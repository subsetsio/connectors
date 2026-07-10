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
    "establishment_type_group",
    "breakdown_topic",
    "breakdown",
    CAST("eligible_pupil_count" AS BIGINT) AS eligible_pupil_count,
    CAST("expected_standard_pupil_count" AS BIGINT) AS expected_standard_pupil_count,
    CAST("expected_standard_pupil_percent" AS BIGINT) AS expected_standard_pupil_percent
FROM "dfe-0f2f9901-dd4d-9f74-b8d3-7933c9f0bba4"
