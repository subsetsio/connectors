-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "C_D___R_E_F_N_I_S" AS c_d_r_e_f_n_i_s,
    "C_D___S_E_C_T_O_R" AS c_d_s_e_c_t_o_r,
    "P_O_P_U_L_A_T_I_O_N" AS p_o_p_u_l_a_t_i_o_n,
    "D_T___S_T_R_T___S_E_C_T_O_R" AS d_t_s_t_r_t_s_e_c_t_o_r,
    "D_T___S_T_O_P___S_E_C_T_O_R" AS d_t_s_t_o_p_s_e_c_t_o_r,
    "O_P_P_E_R_V_L_A_K_T_E___I_N___H_M" AS o_p_p_e_r_v_l_a_k_t_e_i_n_h_m,
    "T_X___D_E_S_C_R___S_E_C_T_O_R___N_L" AS t_x_d_e_s_c_r_s_e_c_t_o_r_n_l,
    "T_X___D_E_S_C_R___S_E_C_T_O_R___F_R" AS t_x_d_e_s_c_r_s_e_c_t_o_r_f_r,
    "T_X___D_E_S_C_R___N_L" AS t_x_d_e_s_c_r_n_l,
    "T_X___D_E_S_C_R___F_R" AS t_x_d_e_s_c_r_f_r
FROM "statbel-nodeid1709"
