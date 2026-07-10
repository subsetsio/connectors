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
    "exam_cohort",
    "qualification_detailed",
    CAST("qualification_level" AS BIGINT) AS qualification_level,
    CAST("a_level_equivelent_size" AS DOUBLE) AS a_level_equivelent_size,
    CAST("gcse_equivelent_size" AS DOUBLE) AS gcse_equivelent_size,
    "grade_structure",
    "subject",
    "grade",
    CAST("entries_count" AS BIGINT) AS entries_count
FROM "dfe-019c2960-5ba9-705a-badb-73986507cd4c"
