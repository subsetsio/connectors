-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("hhid" AS BIGINT) AS hhid,
    CAST("weight" AS DOUBLE) AS weight,
    CAST("psu" AS BIGINT) AS psu,
    CAST("stratum" AS BIGINT) AS stratum,
    CAST("psus_N" AS BIGINT) AS psus_n,
    "CA" AS ca,
    "domain",
    "gp_subdom",
    CAST("extra" AS BIGINT) AS extra,
    CAST("fort" AS BIGINT) AS fort,
    "foodcode",
    "q14_01n",
    "quantity",
    CAST("anncoeff" AS DOUBLE) AS anncoeff,
    CAST("q14_02" AS BIGINT) AS q14_02,
    "q14_03b",
    CAST("q14_03c" AS DOUBLE) AS q14_03c,
    CAST("q14_04a" AS BIGINT) AS q14_04a,
    CAST("q14_04b" AS BIGINT) AS q14_04b,
    CAST("q14_04c" AS BIGINT) AS q14_04c,
    CAST("q14_04d" AS BIGINT) AS q14_04d,
    CAST("q14_04e" AS BIGINT) AS q14_04e,
    CAST("q14_04f" AS BIGINT) AS q14_04f,
    CAST("q14_04g" AS BIGINT) AS q14_04g,
    "q14_05b",
    "source_resource"
FROM "idb-suriname-survey-of-living-conditions-2016-2017"
