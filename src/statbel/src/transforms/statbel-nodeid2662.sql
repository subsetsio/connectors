-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("11000" AS BIGINT) AS "11000",
    CAST("10000" AS BIGINT) AS "10000",
    CAST("2000" AS BIGINT) AS "2000",
    CAST("1" AS BIGINT) AS "1",
    "45_64",
    "1_1_2009_00_00_00",
    CAST("2009" AS BIGINT) AS "2009",
    "2009_W01" AS "2009_w01",
    CAST("2" AS BIGINT) AS "2"
FROM "statbel-nodeid2662"
