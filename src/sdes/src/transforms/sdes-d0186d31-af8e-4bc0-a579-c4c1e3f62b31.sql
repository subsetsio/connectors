-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PRODB_ELE_SYNT" AS prodb_ele_synt,
    "PRODB_HYDRO_SYNT" AS prodb_hydro_synt,
    "PRODB_EOL_SYNT" AS prodb_eol_synt,
    "PRODB_PV_SYNT" AS prodb_pv_synt,
    "PRODB_NUCL_SYNT" AS prodb_nucl_synt,
    "QSOLI_ELE_SYNT" AS qsoli_ele_synt,
    "QIMP_ELE_SYNT" AS qimp_ele_synt,
    "QEXP_ELE_SYNT" AS qexp_ele_synt,
    "CONSO_ELE_SYNT" AS conso_ele_synt,
    "CONSO_ELE_SYNT_COR1" AS conso_ele_synt_cor1,
    "CONSO_ELE_SYNT_COR2" AS conso_ele_synt_cor2,
    "DJU" AS dju,
    "INDRIG" AS indrig
FROM "sdes-d0186d31-af8e-4bc0-a579-c4c1e3f62b31"
