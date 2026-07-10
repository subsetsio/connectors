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
    "region_code",
    "region_name",
    "old_la_code",
    "new_la_code",
    "la_name",
    "breakdown_topic",
    "breakdown",
    "establishment_type_group",
    "establishment_type",
    "exam_cohort",
    "student_count",
    "students_with_prior_count",
    "prior_average"
FROM "dfe-019d9137-8890-76b5-8a80-54824375eeb8"
