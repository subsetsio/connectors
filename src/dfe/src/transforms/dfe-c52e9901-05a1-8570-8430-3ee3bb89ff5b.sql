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
    CAST("establishment_count" AS BIGINT) AS establishment_count,
    "years_open_count",
    CAST("expected_standard_pupil_percent" AS DOUBLE) AS expected_standard_pupil_percent,
    CAST("eligible_pupil_count" AS BIGINT) AS eligible_pupil_count
FROM "dfe-c52e9901-05a1-8570-8430-3ee3bb89ff5b"
