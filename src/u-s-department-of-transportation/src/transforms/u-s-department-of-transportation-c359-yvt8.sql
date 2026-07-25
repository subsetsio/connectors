-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year_record" AS BIGINT) AS year_record,
    CAST("stateid" AS BIGINT) AS stateid,
    "route_id",
    CAST("begin_point" AS DOUBLE) AS begin_point,
    CAST("end_point" AS DOUBLE) AS end_point,
    CAST("section_length" AS DOUBLE) AS section_length,
    CAST("f_system" AS BIGINT) AS f_system,
    "sample_id",
    CAST("expansion_factor" AS DOUBLE) AS expansion_factor,
    "natroute_id",
    CAST("expansion_length" AS DOUBLE) AS expansion_length
FROM "u-s-department-of-transportation-c359-yvt8"
