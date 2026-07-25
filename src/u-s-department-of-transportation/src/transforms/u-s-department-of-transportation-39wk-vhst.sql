-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year_record" AS BIGINT) AS year_record,
    CAST("state_code" AS BIGINT) AS state_code,
    "route_id",
    CAST("begin_point" AS DOUBLE) AS begin_point,
    CAST("end_point" AS DOUBLE) AS end_point,
    "section_length",
    "sample_id",
    CAST("expansion_factor" AS DOUBLE) AS expansion_factor,
    "natroute_id"
FROM "u-s-department-of-transportation-39wk-vhst"
