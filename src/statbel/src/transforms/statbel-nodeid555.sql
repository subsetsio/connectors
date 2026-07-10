-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "Standard_ACE_DB_n_b" AS standard_ace_db_n_b,
    "U_gr___1_y_0_c_F_N_g_7_J" AS u_gr_1_y_0_c_f_n_g_7_j
FROM "statbel-nodeid555"
