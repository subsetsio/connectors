-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This source-form operational extract uses legacy FRA source fields; do not combine it with the curated Form 55 operational table without reconciling duplicate report concepts.
SELECT
    "railroad",
    "iyr",
    "imo",
    "state",
    "county",
    CAST("locomi" AS DOUBLE) AS locomi,
    CAST("mtmi" AS DOUBLE) AS mtmi,
    CAST("ysmi" AS DOUBLE) AS ysmi,
    CAST("totmi" AS DOUBLE) AS totmi,
    CAST("emphrs" AS DOUBLE) AS emphrs,
    CAST("passmi" AS DOUBLE) AS passmi,
    CAST("revpass" AS DOUBLE) AS revpass,
    "typrr",
    CAST("region" AS BIGINT) AS region,
    "dummy",
    CAST("year4" AS BIGINT) AS year4,
    CAST("frtrnmi" AS DOUBLE) AS frtrnmi,
    CAST("pastrnmi" AS DOUBLE) AS pastrnmi,
    CAST("othermi" AS DOUBLE) AS othermi,
    "cntycd",
    "stcnty",
    "narr1",
    "narr2",
    "narr3",
    CAST("narrlen" AS DOUBLE) AS narrlen,
    "dummy1"
FROM "fra-unww-uhxd"
