-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PROD_GAZ_SYNT" AS prod_gaz_synt,
    "QSOLI_GAZ_SYNT" AS qsoli_gaz_synt,
    "CONSO_GAZ_SYNT" AS conso_gaz_synt,
    "CONSO_GAZ_SYNT_COR1" AS conso_gaz_synt_cor1,
    "CONSO_GAZ_SYNT_COR2" AS conso_gaz_synt_cor2,
    "DJU" AS dju,
    "INDRIG" AS indrig
FROM "sdes-c8aef4b9-b362-435f-8a89-1dbdbc561acf"
