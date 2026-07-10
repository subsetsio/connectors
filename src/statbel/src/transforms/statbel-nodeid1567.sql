-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "Standard_Jet_DB_n_b___U_gr___1_y_0_c_F_N_V_7_9_6L_Y_Cv_3_y" AS standard_jet_db_n_b_u_gr_1_y_0_c_f_n_v_7_9_6l_y_cv_3_y,
    "col_1",
    "Y_1___f___g___D_e_F_x___b_T_4_0___p" AS y_1_f_g_d_e_f_x_b_t_4_0_p
FROM "statbel-nodeid1567"
