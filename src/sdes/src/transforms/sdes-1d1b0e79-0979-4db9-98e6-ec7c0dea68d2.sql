-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PX_ELE_I_TRANCHES_IA_IF" AS px_ele_i_tranches_ia_if,
    "PX_ELE_I_IA" AS px_ele_i_ia,
    "PX_ELE_I_IB" AS px_ele_i_ib,
    "PX_ELE_I_IC" AS px_ele_i_ic,
    "PX_ELE_I_ID" AS px_ele_i_id,
    "PX_ELE_I_IE" AS px_ele_i_ie,
    "PX_ELE_I_IF" AS px_ele_i_if,
    "PX_ELE_I_IG" AS px_ele_i_ig,
    "PX_ELE_I_TTES_TRANCHES" AS px_ele_i_ttes_tranches
FROM "sdes-1d1b0e79-0979-4db9-98e6-ec7c0dea68d2"
