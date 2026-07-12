-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "activity_code_rmz_lnsht",
    "nationality",
    "main_economic_activity",
    "compensation_of_employees_value_in_1_000_qr_t_wydt_l_mlyn_lqym_b_lf_ryl_qtry",
    "number_of_employees_dd_lmshtglyn",
    "lnsht_lqtsdy_lry_ysy",
    "ljnsy"
FROM "qatar-planning-and-statistics-authority-hotels-and-restaurants-statistics-number-of-employees-and-compensation-by-nationality-and-economic"
