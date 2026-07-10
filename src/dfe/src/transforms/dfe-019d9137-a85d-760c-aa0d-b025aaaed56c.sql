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
    CAST("student_count" AS BIGINT) AS student_count,
    CAST("achieved_level3_maths_count" AS BIGINT) AS achieved_level3_maths_count,
    CAST("achieved_level3_maths_percent" AS DOUBLE) AS achieved_level3_maths_percent
FROM "dfe-019d9137-a85d-760c-aa0d-b025aaaed56c"
