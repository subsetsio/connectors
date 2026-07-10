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
    "cohort",
    "student_count",
    "aps_per_entry",
    "aps_per_entry_grade"
FROM "dfe-019d9133-f62c-722e-b878-282fd582d625"
