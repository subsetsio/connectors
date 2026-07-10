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
    "ethnicity_major",
    "placement",
    "version",
    "subject",
    "eligible_pupil_count",
    "expected_standard_pupil_count",
    "expected_standard_pupil_percent",
    "progress_measure_eligible_pupil_count",
    "progress_measure_total_score",
    "progress_measure_score",
    "progress_measure_lower_conf_interval",
    "progress_measure_upper_conf_interval"
FROM "dfe-019d431f-c129-73e6-917e-6998bfe4d88d"
