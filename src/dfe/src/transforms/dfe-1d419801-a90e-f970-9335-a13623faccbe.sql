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
    "region_code",
    "region_name",
    "apprenticeship_level",
    "age_youth_adult",
    "age_group",
    "funding_type",
    "provider_type",
    "start_count",
    "achievement_count",
    "participation_count",
    "starts_percent",
    "achievements_percent"
FROM "dfe-1d419801-a90e-f970-9335-a13623faccbe"
