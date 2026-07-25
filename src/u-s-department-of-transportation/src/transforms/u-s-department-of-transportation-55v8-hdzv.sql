-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("datayear" AS BIGINT) AS datayear,
    CAST("stateid" AS BIGINT) AS stateid,
    CAST("urbanid" AS BIGINT) AS urbanid,
    CAST("vmt" AS BIGINT) AS vmt
FROM "u-s-department-of-transportation-55v8-hdzv"
