-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    CAST("objectid" AS BIGINT) AS objectid,
    "city_name",
    CAST("pop" AS BIGINT) AS pop,
    CAST("pop_rank" AS BIGINT) AS pop_rank,
    "pop_class",
    CAST("label_flag" AS BIGINT) AS label_flag
FROM "u-s-department-of-transportation-225h-8raq"
