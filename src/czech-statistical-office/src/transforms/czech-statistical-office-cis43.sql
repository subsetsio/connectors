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
    "obec_ul",
    "ob_ul_cor",
    CAST("sm_rozsah" AS BIGINT) AS sm_rozsah,
    CAST("sm_typ" AS BIGINT) AS sm_typ,
    "kodobce_h",
    "domin_cobc",
    CAST("porcobec_o" AS BIGINT) AS porcobec_o
FROM "czech-statistical-office-cis43"
