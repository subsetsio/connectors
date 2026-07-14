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
    strptime("admnepo", '%Y-%m-%d')::DATE AS admnepo,
    "vykhmot",
    regexp_extract(
        "predchudce""predchudce""predchudce""predchudce""predchudce""predchudce""predchudce""predchudce""predchudce""predchudce""predchudce""predchudce",
        '^[^"]+'
    ) AS predecessor_code
FROM "czech-statistical-office-cis5585"
