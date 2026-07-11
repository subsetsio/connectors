-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "typuz_naz",
    "nazev",
    CAST("uzcis" AS BIGINT) AS uzcis,
    CAST("uzkod" AS BIGINT) AS uzkod,
    CAST("u01" AS DOUBLE) AS u01,
    CAST("u02" AS DOUBLE) AS u02,
    CAST("u03" AS DOUBLE) AS u03,
    CAST("u04" AS DOUBLE) AS u04,
    CAST("u05" AS DOUBLE) AS u05,
    CAST("u06" AS DOUBLE) AS u06,
    CAST("u07" AS DOUBLE) AS u07,
    CAST("u08" AS DOUBLE) AS u08,
    CAST("u09" AS DOUBLE) AS u09,
    CAST("u10" AS DOUBLE) AS u10,
    CAST("u11" AS DOUBLE) AS u11
FROM "czech-statistical-office-sldb2011-zakladni"
