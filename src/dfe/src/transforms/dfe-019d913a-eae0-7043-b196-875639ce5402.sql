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
    "establishment_type_group",
    "establishment_type",
    "subject_area",
    "subject",
    "grade",
    "grade_count",
    "grade_percent",
    "astar_to_grade_cumulative_count",
    "astar_to_grade_cumulative_percent"
FROM "dfe-019d913a-eae0-7043-b196-875639ce5402"
