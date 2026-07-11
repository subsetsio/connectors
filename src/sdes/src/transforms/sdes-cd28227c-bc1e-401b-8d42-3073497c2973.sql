-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PX_ELE_D_TTES_TRANCHES" AS px_ele_d_ttes_tranches,
    "PX_ELE_D_DA" AS px_ele_d_da,
    "PX_ELE_D_DB" AS px_ele_d_db,
    "PX_ELE_D_DC" AS px_ele_d_dc,
    "PX_ELE_D_DD" AS px_ele_d_dd,
    "PX_ELE_D_DE" AS px_ele_d_de
FROM "sdes-cd28227c-bc1e-401b-8d42-3073497c2973"
