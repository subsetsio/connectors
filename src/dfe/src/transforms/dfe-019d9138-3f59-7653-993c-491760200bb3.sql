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
    "trust_type",
    "performance_tables_eligibility",
    "academy_type",
    "breakdown_topic",
    "breakdown",
    "exam_cohort",
    "institution_count",
    "student_count",
    "aps_per_entry",
    "value_added",
    "entries_count"
FROM "dfe-019d9138-3f59-7653-993c-491760200bb3"
