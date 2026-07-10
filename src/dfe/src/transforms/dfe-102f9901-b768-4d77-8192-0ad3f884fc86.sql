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
    "sex",
    "subject",
    "scaled_scores",
    CAST("eligible_pupil_count" AS BIGINT) AS eligible_pupil_count,
    CAST("cumulative_percent" AS BIGINT) AS cumulative_percent
FROM "dfe-102f9901-b768-4d77-8192-0ad3f884fc86"
