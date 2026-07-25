-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("datayear" AS BIGINT) AS datayear,
    CAST("stateid" AS BIGINT) AS stateid,
    CAST("countyid" AS BIGINT) AS countyid,
    CAST("fsystem" AS BIGINT) AS fsystem,
    CAST("urbanid" AS BIGINT) AS urbanid,
    CAST("ownership" AS BIGINT) AS ownership,
    CAST("systemlength" AS DOUBLE) AS systemlength
FROM "u-s-department-of-transportation-8j5p-a5aj"
