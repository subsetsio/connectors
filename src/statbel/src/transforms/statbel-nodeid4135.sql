-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "Standard_Jet_DB_n_b" AS standard_jet_db_n_b,
    "U_gr___1_y_0_c_F_N" AS u_gr_1_y_0_c_f_n
FROM "statbel-nodeid4135"
