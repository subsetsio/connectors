-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "type_of_compensation",
    "occupation",
    "compensation_of_employees_value_in_1_000_qr_t_wydt_l_mlyn_lqym_b_lf_ryl_qtry",
    "lmhn",
    "nw_lt_wyd"
FROM "qatar-planning-and-statistics-authority-hotels-and-restaurants-statistics-estimates-of-compensation-in-hotels-and-restaurants-by-occupation0"
