-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    CAST("EFDELEV" AS BIGINT) AS efdelev,
    "XEFDETOT" AS xefdetot,
    CAST("EFDETOT" AS BIGINT) AS efdetot,
    "XEFDEEXC" AS xefdeexc,
    "EFDEEXC" AS efdeexc,
    "XEFDESOM" AS xefdesom,
    "EFDESOM" AS efdesom,
    "XEFDENON" AS xefdenon,
    "EFDENON" AS efdenon,
    "XEFDEEX1" AS xefdeex1,
    "EFDEEX1" AS efdeex1,
    "XEFDEEX2" AS xefdeex2,
    "EFDEEX2" AS efdeex2,
    "XEFDEEX3" AS xefdeex3,
    "EFDEEX3" AS efdeex3,
    "XEFDEEX4" AS xefdeex4,
    "EFDEEX4" AS efdeex4,
    "XEFDEEX5" AS xefdeex5,
    "EFDEEX5" AS efdeex5,
    "year"
FROM "nces-ipeds-efa-dist"
