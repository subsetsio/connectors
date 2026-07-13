-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("folio_anon" AS BIGINT) AS folio_anon,
    CAST("id_s8" AS BIGINT) AS id_s8,
    "P08_1" AS p08_1,
    "P08_2" AS p08_2,
    "P08_3A" AS p08_3a,
    "P08_3B" AS p08_3b,
    CAST("P08_4" AS BIGINT) AS p08_4,
    "P08_6" AS p08_6,
    "P08_7A" AS p08_7a,
    "P08_7B" AS p08_7b,
    CAST("P08_8" AS BIGINT) AS p08_8,
    "P08_10" AS p08_10,
    "P08_11A" AS p08_11a,
    "P08_11B" AS p08_11b,
    CAST("P08_12" AS BIGINT) AS p08_12,
    "source_resource"
FROM "idb-community-nutrition-program-in-el-alto-bolivia-data-2014-2017"
