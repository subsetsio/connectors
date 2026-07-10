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
    CAST("sublevno" AS BIGINT) AS sublevno,
    "qualification_detailed",
    CAST("a_level_equivelent_size" AS DOUBLE) AS a_level_equivelent_size,
    "subject_code",
    "subject",
    "value_added",
    "value_added_lower_ci",
    "value_added_upper_ci",
    "entries_count"
FROM "dfe-019c2960-abc0-700e-91ed-bb9823c0feed"
