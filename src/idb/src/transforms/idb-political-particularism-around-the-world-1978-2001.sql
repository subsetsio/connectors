-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idcode" AS BIGINT) AS idcode,
    "country",
    CAST("bicameral" AS BIGINT) AS bicameral,
    CAST("year" AS BIGINT) AS year,
    CAST("oneparty" AS BIGINT) AS oneparty,
    "ballot",
    "pool",
    CAST("vote" AS DOUBLE) AS vote,
    "cindex",
    CAST("dm" AS DOUBLE) AS dm,
    "smd",
    "propn",
    CAST("ballot2" AS BIGINT) AS ballot2,
    CAST("pool2" AS DOUBLE) AS pool2,
    CAST("vote2" AS DOUBLE) AS vote2,
    "cindex2",
    CAST("dm2" AS DOUBLE) AS dm2,
    "smd2",
    "propn2",
    "source_resource"
FROM "idb-political-particularism-around-the-world-1978-2001"
