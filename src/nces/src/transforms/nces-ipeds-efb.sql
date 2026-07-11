-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    "EFBAGE" AS efbage,
    CAST("LINE" AS BIGINT) AS line,
    "LSTUDY" AS lstudy,
    "XEFAGE01" AS xefage01,
    "EFAGE01" AS efage01,
    "XEFAGE02" AS xefage02,
    "EFAGE02" AS efage02,
    "XEFAGE03" AS xefage03,
    "EFAGE03" AS efage03,
    "XEFAGE04" AS xefage04,
    "EFAGE04" AS efage04,
    "XEFAGE05" AS xefage05,
    "EFAGE05" AS efage05,
    "XEFAGE06" AS xefage06,
    "EFAGE06" AS efage06,
    "XEFAGE07" AS xefage07,
    "EFAGE07" AS efage07,
    "XEFAGE08" AS xefage08,
    "EFAGE08" AS efage08,
    "XEFAGE09" AS xefage09,
    "EFAGE09" AS efage09,
    "year"
FROM "nces-ipeds-efb"
