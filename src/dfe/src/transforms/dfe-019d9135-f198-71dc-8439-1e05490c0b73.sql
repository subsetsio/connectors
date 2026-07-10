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
    "subject",
    "qualification_type",
    "qualification",
    "student_count",
    CAST("student_pass_count" AS BIGINT) AS student_pass_count,
    "student_pass_percent"
FROM "dfe-019d9135-f198-71dc-8439-1e05490c0b73"
