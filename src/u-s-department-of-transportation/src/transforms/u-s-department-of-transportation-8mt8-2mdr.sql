-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("unique_id" AS BIGINT) AS unique_id,
    "insp_date",
    CAST("dot_number" AS BIGINT) AS dot_number,
    "viol_code",
    "basic_desc",
    CAST("oos_indicator" AS BOOLEAN) AS oos_indicator,
    CAST("oos_weight" AS BIGINT) AS oos_weight,
    CAST("severity_weight" AS BIGINT) AS severity_weight,
    CAST("time_weight" AS BIGINT) AS time_weight,
    CAST("total_severity_wght" AS BIGINT) AS total_severity_wght,
    "section_desc",
    "group_desc",
    "viol_unit"
FROM "u-s-department-of-transportation-8mt8-2mdr"
