-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PROD_PETRO_SYNT" AS prod_petro_synt,
    "QSOLI_PETRO_SYNT" AS qsoli_petro_synt,
    "QIMP_PETRO_SYNT" AS qimp_petro_synt,
    "QIMP_BRUT_SYNT" AS qimp_brut_synt,
    "QIMP_RAFF_SYNT" AS qimp_raff_synt,
    "QEXP_RAFF_SYNT" AS qexp_raff_synt,
    "QSOLI_RAFF_SYNT" AS qsoli_raff_synt,
    "SOUTESMAR_SYNT" AS soutesmar_synt,
    "CONSO_PETRO_SYNT" AS conso_petro_synt,
    "CONSO_PETRO_COR1_SYNT" AS conso_petro_cor1_synt,
    "CONSO_PETRO_COR2_SYNT" AS conso_petro_cor2_synt,
    "DJU" AS dju,
    "INDRIG" AS indrig
FROM "sdes-26173fee-8ca4-40f5-a8bd-746bc9dda1b0"
