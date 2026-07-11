-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_member",
    "typuz_naz",
    "nazev",
    CAST("uzcis" AS BIGINT) AS uzcis,
    CAST("uzkod" AS BIGINT) AS uzkod,
    CAST("vse10111" AS DOUBLE) AS vse10111,
    CAST("vse10121" AS DOUBLE) AS vse10121,
    CAST("vse10131" AS DOUBLE) AS vse10131,
    CAST("vse10141" AS DOUBLE) AS vse10141,
    CAST("vse10151" AS DOUBLE) AS vse10151,
    CAST("vse10161" AS DOUBLE) AS vse10161,
    CAST("vse10171" AS DOUBLE) AS vse10171,
    CAST("vse10181" AS DOUBLE) AS vse10181,
    CAST("vse10191" AS DOUBLE) AS vse10191
FROM "czech-statistical-office-sldbdomac"
