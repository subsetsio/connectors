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
    "old_la_code",
    "new_la_code",
    "la_name",
    "version",
    "establishment_type_group",
    "breakdown_topic",
    "breakdown",
    "subject",
    "expected_standard_pupil_percent",
    "higher_standard_pupil_percent",
    "average_scaled_score",
    "progress_measure_score",
    "progress_measure_lower_conf_interval",
    "progress_measure_upper_conf_interval",
    "absent_or_not_able_to_access_percent",
    "working_towards_expected_standard_pupil_percent",
    "absent_or_disapplied_percent",
    "progress_measure_unadjusted",
    "progress_measure_description"
FROM "dfe-019afee5-4791-7467-a788-c163fd9b57de"
