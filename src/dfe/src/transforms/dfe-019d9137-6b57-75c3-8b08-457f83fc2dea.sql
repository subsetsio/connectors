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
    "establishment_type_group",
    "establishment_type",
    "sex",
    "exam_cohort",
    CAST("student_count" AS BIGINT) AS student_count,
    CAST("students_with_prior_count" AS BIGINT) AS students_with_prior_count,
    "prior_average"
FROM "dfe-019d9137-6b57-75c3-8b08-457f83fc2dea"
