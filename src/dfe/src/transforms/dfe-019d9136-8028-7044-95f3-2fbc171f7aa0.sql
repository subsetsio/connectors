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
    "breakdown_topic",
    "breakdown",
    "subject",
    CAST("student_count" AS BIGINT) AS student_count,
    "baseline_average",
    "progress_average",
    "entering_percent",
    "improving_pecent",
    "same_percent",
    "lower_percent",
    "non_entry_percent",
    "grade_four_plus_percent"
FROM "dfe-019d9136-8028-7044-95f3-2fbc171f7aa0"
