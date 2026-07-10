-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Arrival ATFM delay is split across total and cause-code columns in the same airport-day row; summing all delay columns together would double count.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH_NUM" AS BIGINT) AS month_num,
    "MONTH_MON" AS month_mon,
    "FLT_DATE" AS flt_date,
    "APT_ICAO" AS apt_icao,
    "APT_NAME" AS apt_name,
    "STATE_NAME" AS state_name,
    "ATFM_VERSION" AS atfm_version,
    CAST("FLT_ARR_1" AS BIGINT) AS flt_arr_1,
    "DLY_APT_ARR_1" AS dly_apt_arr_1,
    "DLY_APT_ARR_A_1" AS dly_apt_arr_a_1,
    "DLY_APT_ARR_C_1" AS dly_apt_arr_c_1,
    "DLY_APT_ARR_D_1" AS dly_apt_arr_d_1,
    "DLY_APT_ARR_E_1" AS dly_apt_arr_e_1,
    "DLY_APT_ARR_G_1" AS dly_apt_arr_g_1,
    "DLY_APT_ARR_I_1" AS dly_apt_arr_i_1,
    "DLY_APT_ARR_M_1" AS dly_apt_arr_m_1,
    "DLY_APT_ARR_N_1" AS dly_apt_arr_n_1,
    "DLY_APT_ARR_O_1" AS dly_apt_arr_o_1,
    "DLY_APT_ARR_P_1" AS dly_apt_arr_p_1,
    "DLY_APT_ARR_R_1" AS dly_apt_arr_r_1,
    "DLY_APT_ARR_S_1" AS dly_apt_arr_s_1,
    "DLY_APT_ARR_T_1" AS dly_apt_arr_t_1,
    "DLY_APT_ARR_V_1" AS dly_apt_arr_v_1,
    "DLY_APT_ARR_W_1" AS dly_apt_arr_w_1,
    "DLY_APT_ARR_NA_1" AS dly_apt_arr_na_1,
    "FLT_ARR_1_DLY" AS flt_arr_1_dly,
    "FLT_ARR_1_DLY_15" AS flt_arr_1_dly_15,
    "OBS_DATE" AS obs_date
FROM "eurocontrol-apt-dly"
