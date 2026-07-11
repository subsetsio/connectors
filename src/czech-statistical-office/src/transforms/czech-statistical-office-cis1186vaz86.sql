-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kodjaz",
    "typvaz",
    "akrcis1",
    CAST("kodcis1" AS BIGINT) AS kodcis1,
    "chodnota1",
    "text1",
    "akrcis2",
    CAST("kodcis2" AS BIGINT) AS kodcis2,
    "chodnota2",
    "text2"
FROM "czech-statistical-office-cis1186vaz86"
