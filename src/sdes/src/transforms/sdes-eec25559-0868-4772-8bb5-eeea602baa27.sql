-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PRODRES_GAZ" AS prodres_gaz,
    "QSOLI_GAZ" AS qsoli_gaz,
    "QIMP_GAZ" AS qimp_gaz,
    "QIMPNOR_GAZ" AS qimpnor_gaz,
    "QIMPALG_GAZ" AS qimpalg_gaz,
    "QIMPRUS_GAZ" AS qimprus_gaz,
    "QIMPNL_GAZ" AS qimpnl_gaz,
    "QIMPNIG_GAZ" AS qimpnig_gaz,
    "QIMPQAT_GAZ" AS qimpqat_gaz,
    "QIMPUSA_GAZ" AS qimpusa_gaz,
    "VSTO_GAZ" AS vsto_gaz,
    "CONSO_GAZ" AS conso_gaz,
    "LTRAN_GAZ" AS ltran_gaz,
    "LPE_GAZ" AS lpe_gaz,
    "LDIS_GAZ" AS ldis_gaz,
    "CONSO_GAZ_COR1" AS conso_gaz_cor1,
    "CTRAN_GAZ_COR1" AS ctran_gaz_cor1,
    "CDIS_GAZ_COR1" AS cdis_gaz_cor1,
    "CONSO_GAZ_COR2" AS conso_gaz_cor2,
    "CTRAN_GAZ_COR2" AS ctran_gaz_cor2,
    "CDIS_GAZ_COR2" AS cdis_gaz_cor2,
    "STO_GAZ" AS sto_gaz,
    "PRODBIO_GAZ" AS prodbio_gaz,
    "DJU" AS dju,
    "INDRIG" AS indrig
FROM "sdes-eec25559-0868-4772-8bb5-eeea602baa27"
