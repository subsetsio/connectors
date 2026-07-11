-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PRODB_ELE" AS prodb_ele,
    "PRODN_ELE" AS prodn_ele,
    "PRODB_NUCL" AS prodb_nucl,
    "PRODN_NUCL" AS prodn_nucl,
    "PRODB_HYDRO" AS prodb_hydro,
    "PRODN_HYDRO" AS prodn_hydro,
    "PRODB_EOL" AS prodb_eol,
    "PRODN_EOL" AS prodn_eol,
    "PRODB_PV" AS prodb_pv,
    "PRODN_PV" AS prodn_pv,
    "PRODB_ELE_THERM" AS prodb_ele_therm,
    "PRODN_ELE_THERM" AS prodn_ele_therm,
    "STEP_ELE" AS step_ele,
    "QIMP_ELE" AS qimp_ele,
    "QEXP_ELE" AS qexp_ele,
    "EAR_ELE" AS ear_ele,
    "LIV_ELE_BT" AS liv_ele_bt,
    "LIV_ELE_MT" AS liv_ele_mt,
    "LIV_ELE_HT" AS liv_ele_ht,
    "PUISSMAX_ELE" AS puissmax_ele,
    "QSOLI_ELE" AS qsoli_ele,
    "CONSO_ELE_COR1" AS conso_ele_cor1,
    "LIV_ELE_BT_COR1" AS liv_ele_bt_cor1,
    "LIV_ELE_MT_COR1" AS liv_ele_mt_cor1,
    "LIV_ELE_HT_COR1" AS liv_ele_ht_cor1,
    "CONSO_ELE_COR2" AS conso_ele_cor2,
    "LIV_ELE_BT_COR2" AS liv_ele_bt_cor2,
    "LIV_ELE_MT_COR2" AS liv_ele_mt_cor2,
    "LIV_ELE_HT_COR2" AS liv_ele_ht_cor2,
    "DJU" AS dju,
    "INDRIG" AS indrig
FROM "sdes-691526bb-4148-4f34-b465-4d5223a0172c"
