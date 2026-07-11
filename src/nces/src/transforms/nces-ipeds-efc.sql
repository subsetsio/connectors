-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    "EFCSTATE" AS efcstate,
    CAST("LINE" AS BIGINT) AS line,
    "XEFRES01" AS xefres01,
    CAST("EFRES01" AS BIGINT) AS efres01,
    "XEFRES02" AS xefres02,
    "EFRES02" AS efres02,
    "year"
FROM "nces-ipeds-efc"
