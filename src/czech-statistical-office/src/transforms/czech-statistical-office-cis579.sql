-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kodjaz",
    "akrcis",
    CAST("kodcis" AS BIGINT) AS kodcis,
    "chodnota",
    "zkrtext",
    "text",
    strptime("admplod", '%Y-%m-%d')::DATE AS admplod,
    strptime("admnepo", '%Y-%m-%d')::DATE AS admnepo
FROM "czech-statistical-office-cis579"
