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
    "education_phase",
    "school_religious_character",
    "sex",
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
FROM "dfe-019a970a-4cf3-762d-9e22-af794d1cb2cb"
