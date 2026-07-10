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
    "performance_tables_eligibility",
    "trust_type",
    "establishment_type_group",
    "breakdown_topic",
    "breakdown",
    "subject",
    CAST("establishment_count" AS BIGINT) AS establishment_count,
    CAST("cohort_pupil_count" AS BIGINT) AS cohort_pupil_count,
    CAST("eligible_pupil_count" AS BIGINT) AS eligible_pupil_count,
    "progress_measure_eligible_pupil_count",
    CAST("expected_standard_pupil_percent" AS BIGINT) AS expected_standard_pupil_percent,
    "progress_measure_score",
    "progress_measure_upper_conf_interval",
    "progress_measure_lower_conf_interval"
FROM "dfe-019afee5-aa60-75a8-94ea-bcb76c2c9384"
