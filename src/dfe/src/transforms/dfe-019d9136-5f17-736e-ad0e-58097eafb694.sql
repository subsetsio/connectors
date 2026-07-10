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
    "subject",
    CAST("student_count" AS BIGINT) AS student_count,
    CAST("baseline_average" AS DOUBLE) AS baseline_average,
    CAST("progress_average" AS DOUBLE) AS progress_average,
    CAST("entering_percent" AS DOUBLE) AS entering_percent,
    CAST("improving_pecent" AS DOUBLE) AS improving_pecent,
    CAST("same_percent" AS DOUBLE) AS same_percent,
    CAST("lower_percent" AS DOUBLE) AS lower_percent,
    CAST("non_entry_percent" AS DOUBLE) AS non_entry_percent,
    CAST("grade_four_plus_percent" AS DOUBLE) AS grade_four_plus_percent
FROM "dfe-019d9136-5f17-736e-ad0e-58097eafb694"
