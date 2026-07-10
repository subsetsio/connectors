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
    "social_care_group",
    "sen_provision",
    "sen_primary_need",
    "pupil_count",
    "pupil_percent"
FROM "dfe-019d431f-f58f-73c2-9c1e-5e5fd3462e77"
