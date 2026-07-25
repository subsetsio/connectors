-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tbl",
    CAST("year" AS BIGINT) AS year,
    CAST("quarter" AS BIGINT) AS quarter,
    CAST("citymarketid" AS BIGINT) AS citymarketid,
    "cityname",
    CAST("airportid" AS BIGINT) AS airportid,
    "apt",
    CAST("totalmkts" AS BIGINT) AS totalmkts,
    CAST("totalfaredpax" AS BIGINT) AS totalfaredpax,
    CAST("totalperlfmkts" AS DOUBLE) AS totalperlfmkts,
    CAST("totalavghubfare" AS DOUBLE) AS totalavghubfare,
    CAST("totalperprem" AS DOUBLE) AS totalperprem,
    CAST("shmkts" AS BIGINT) AS shmkts,
    CAST("shpax" AS BIGINT) AS shpax,
    CAST("shperlfmkts" AS DOUBLE) AS shperlfmkts,
    CAST("shavghubfare" AS DOUBLE) AS shavghubfare,
    CAST("shperprem" AS DOUBLE) AS shperprem,
    CAST("lhmkts" AS BIGINT) AS lhmkts,
    CAST("lhpax" AS BIGINT) AS lhpax,
    CAST("lhperlfmkts" AS DOUBLE) AS lhperlfmkts,
    CAST("lhavghubfare" AS DOUBLE) AS lhavghubfare,
    CAST("lhperprem" AS DOUBLE) AS lhperprem,
    "tbl7pk"
FROM "u-s-department-of-transportation-d6nc-s8v6"
