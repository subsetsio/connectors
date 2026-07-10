-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are the FIR-boundary view of en-route ATFM delay; do not add them to the ANSP/AUA view as if they were disjoint geographies.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH_NUM" AS BIGINT) AS month_num,
    "MONTH_MON" AS month_mon,
    "FLT_DATE" AS flt_date,
    "ENTITY_NAME" AS entity_name,
    "ENTITY_TYPE" AS entity_type,
    CAST("FLT_ERT_1" AS BIGINT) AS flt_ert_1,
    "DLY_ERT_1" AS dly_ert_1,
    "DLY_ERT_A_1" AS dly_ert_a_1,
    "DLY_ERT_C_1" AS dly_ert_c_1,
    "DLY_ERT_D_1" AS dly_ert_d_1,
    "DLY_ERT_E_1" AS dly_ert_e_1,
    "DLY_ERT_G_1" AS dly_ert_g_1,
    "DLY_ERT_I_1" AS dly_ert_i_1,
    "DLY_ERT_M_1" AS dly_ert_m_1,
    "DLY_ERT_N_1" AS dly_ert_n_1,
    "DLY_ERT_O_1" AS dly_ert_o_1,
    "DLY_ERT_P_1" AS dly_ert_p_1,
    "DLY_ERT_R_1" AS dly_ert_r_1,
    "DLY_ERT_S_1" AS dly_ert_s_1,
    "DLY_ERT_T_1" AS dly_ert_t_1,
    "DLY_ERT_V_1" AS dly_ert_v_1,
    "DLY_ERT_W_1" AS dly_ert_w_1,
    "DLY_ERT_NA_1" AS dly_ert_na_1,
    "FLT_ERT_1_DLY" AS flt_ert_1_dly,
    "FLT_ERT_1_DLY_15" AS flt_ert_1_dly_15,
    "OBS_DATE" AS obs_date
FROM "eurocontrol-ert-dly-fir"
