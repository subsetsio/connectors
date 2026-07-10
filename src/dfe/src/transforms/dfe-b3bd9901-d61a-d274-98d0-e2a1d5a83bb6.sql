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
    "disadvantage_status",
    "ethnicity_major",
    "ethnicity_minor",
    "first_language",
    "fsm_status",
    "month_of_birth",
    "sen_provision",
    "sen_primary_need",
    "year_group",
    "establishment_count",
    "eligible_pupil_count",
    "expected_standard_pupil_count",
    "working_towards_pupil_count",
    "absent_pupil_count",
    "disapplied_pupil_count",
    "expected_standard_pupil_percent",
    "working_towards_pupil_percent",
    "absent_pupil_percent",
    "disapplied_pupil_percent"
FROM "dfe-b3bd9901-d61a-d274-98d0-e2a1d5a83bb6"
