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
    CAST("vse9111" AS DOUBLE) AS vse9111,
    CAST("vse9121" AS DOUBLE) AS vse9121,
    CAST("vse9131" AS DOUBLE) AS vse9131,
    CAST("vse9141" AS DOUBLE) AS vse9141,
    CAST("vse9151" AS DOUBLE) AS vse9151,
    CAST("vse9161" AS DOUBLE) AS vse9161,
    CAST("vse9171" AS DOUBLE) AS vse9171,
    CAST("vse9181" AS DOUBLE) AS vse9181,
    CAST("vse9191" AS DOUBLE) AS vse9191,
    CAST("vse91101" AS DOUBLE) AS vse91101
FROM "czech-statistical-office-sldbvyjizdka"
