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
    CAST("old_la_code" AS BIGINT) AS old_la_code,
    "new_la_code",
    "la_name",
    "school_name",
    CAST("school_urn" AS BIGINT) AS school_urn,
    CAST("school_laestab" AS BIGINT) AS school_laestab,
    "exam_cohort",
    "qualification_detailed",
    CAST("qualification_level" AS BIGINT) AS qualification_level,
    CAST("a_level_equivelent_size" AS DOUBLE) AS a_level_equivelent_size,
    CAST("gcse_equivelent_size" AS DOUBLE) AS gcse_equivelent_size,
    "grade_structure",
    "subject",
    "grade",
    "entries_count"
FROM "dfe-019c2960-df54-772f-8ad4-a2bc3d3b134f"
