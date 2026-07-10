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
    "region_name",
    "region_code",
    "old_la_code",
    "la_name",
    "new_la_code",
    "pcon_code",
    "pcon_name",
    "phase_type_grouping",
    "sen_provision",
    "sen_primary_need",
    "ethnicity_major",
    "ethnicity_minor",
    CAST("pupil_count" AS BIGINT) AS pupil_count,
    CAST("pupil_percent" AS DOUBLE) AS pupil_percent
FROM "dfe-019df85c-f5a6-7217-87ff-6ef033fc1e9c"
