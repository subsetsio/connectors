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
    CAST("establishment_count" AS BIGINT) AS establishment_count,
    "eligible_pupil_count",
    "completed_check_pupil_count",
    "not_completed_check_pupil_count",
    "absent_pupil_count",
    "unable_to_participate_pupil_count",
    "working_below_pupil_count",
    "just_arrived_pupil_count",
    "missing_reason_pupil_count",
    "mtc_score_total",
    "mtc_score_average",
    "completed_check_pupil_percent",
    "not_completed_check_pupil_percent",
    "absent_pupil_percent",
    "unable_to_participate_pupil_percent",
    "working_below_pupil_percent",
    "just_arrived_pupil_percent",
    "missing_reason_pupil_percent"
FROM "dfe-019a838e-29ef-73ae-8a1d-6df5e1dda10c"
