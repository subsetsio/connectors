-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    "XCDACTUA" AS xcdactua,
    "CDACTUA" AS cdactua,
    "XCNACTUA" AS xcnactua,
    "CNACTUA" AS cnactua,
    "XCDACTGA" AS xcdactga,
    "CDACTGA" AS cdactga,
    "XEFTEUG" AS xefteug,
    "EFTEUG" AS efteug,
    "XEFTEGD" AS xeftegd,
    "EFTEGD" AS eftegd,
    "XFTEUG" AS xfteug,
    "FTEUG" AS fteug,
    "XFTEGD" AS xftegd,
    "FTEGD" AS ftegd,
    "XFTEDPP" AS xftedpp,
    "FTEDPP" AS ftedpp,
    "ACTTYPE" AS acttype,
    "year"
FROM "nces-ipeds-efia"
