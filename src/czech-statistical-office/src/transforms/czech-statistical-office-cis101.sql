-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kodjaz",
    "akrcis",
    CAST("kodcis" AS BIGINT) AS kodcis,
    CAST("chodnota" AS BIGINT) AS chodnota,
    "zkrtext",
    "text",
    strptime("admplod", '%Y-%m-%d')::DATE AS admplod,
    strptime("admnepo", '%Y-%m-%d')::DATE AS admnepo,
    "cznuts",
    "okres_lau",
    CAST("kraj_1960" AS BIGINT) AS kraj_1960,
    CAST("kod_ruian" AS BIGINT) AS kod_ruian
FROM "czech-statistical-office-cis101"
