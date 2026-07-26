-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "_location" AS location,
    "s1_label_a_fy14_revised_base",
    "s1_label_b_fsf_tl_09_c4e_ctt",
    "s1_label_c_fsf_over_formula",
    "s2_label_d_fsf_preliminary",
    "s2_label_a_fy14_revised_base",
    "s2_label_f_register_change",
    "s2_label_g_teacher_salary_growth",
    "s2_label_h_new_school_foundation",
    "s3_label_i_fy14_fsf_at_100",
    "s3_foundation",
    "s3_label_d_foundation",
    "s3_label_i_foundation",
    "s3_label_j_fsf_final",
    "s4_label_d_fy14_fsf_initial",
    "s4_ac_name_fsf_hs",
    "s4_ac_name_tl09_c4e_ctt_hs",
    "s4_ac_name_funds_over_formula",
    "s5_tl_se_transitional_funding",
    "as_of_date"
FROM "nyc-open-data-ven4-h25u"
