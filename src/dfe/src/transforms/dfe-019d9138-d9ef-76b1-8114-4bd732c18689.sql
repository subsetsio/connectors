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
    "prior_attainment",
    "establishment_type_group",
    "establishment_type",
    "exam_cohort",
    "qualification_level",
    CAST("retained_student_count" AS BIGINT) AS retained_student_count,
    CAST("retained_percent" AS DOUBLE) AS retained_percent
FROM "dfe-019d9138-d9ef-76b1-8114-4bd732c18689"
