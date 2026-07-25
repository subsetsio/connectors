-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("stateid" AS BIGINT) AS stateid,
    CAST("urbanid" AS BIGINT) AS urbanid,
    CAST("fsystem" AS BIGINT) AS fsystem,
    CAST("vmt" AS BIGINT) AS vmt
FROM "u-s-department-of-transportation-d84g-cswr"
