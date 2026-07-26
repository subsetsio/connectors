-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "_location" AS location,
    "print_order",
    "attribute_reference",
    "attribute_category",
    "need_name",
    "category",
    "sub_category",
    "column_l_fy15_weight",
    "column_m_fy15_per_capita_no_ats_growth",
    "column_n_fy14_actual_registers",
    "column_o_projected_register",
    "column_p_projected_formula",
    "column_q_register_change",
    "column_r_register_dollar_change"
FROM "nyc-open-data-wr4r-bue7"
