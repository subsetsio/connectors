-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "Standard_Jet_DB_n_b" AS standard_jet_db_n_b,
    "U_gr___1_y_0_c_F_N_T_7z_4_s_6_P_C_3_y___i__f___g___D_e_F_x___b_T_4_0_v_____Y_S____Y" AS u_gr_1_y_0_c_f_n_t_7z_4_s_6_p_c_3_y_i_f_g_d_e_f_x_b_t_4_0_v_y_s_y,
    "col_2",
    "Y" AS y,
    "Y_1" AS y_1,
    "col_5"
FROM "statbel-nodeid4779"
