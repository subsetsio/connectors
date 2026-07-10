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
    CAST("school_urn" AS BIGINT) AS school_urn,
    CAST("school_laestab" AS BIGINT) AS school_laestab,
    "school_name",
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
FROM "dfe-019afee4-e5d0-72f9-9a8f-d7a1a56eac1d"
