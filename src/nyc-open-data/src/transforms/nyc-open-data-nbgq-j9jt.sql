-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "_location" AS location,
    "total_column_n_fy14_actual_registers",
    "total_column_o_projected_register",
    "total_column_p_projected_formula",
    "total_column_q_register_change",
    "total_column_r_register_dollar_change",
    "weighted_register",
    "systemwide_teacher_salary_growth",
    "label_g_teacher_salary_growth",
    "foundation",
    "label_j_fy15_fair_student_formula_at_100",
    "label_a_fy14_revised_based_allocations",
    "label_s_fair_student_funding_register_formula",
    "label_t_change_to_preliminary_fair_student_funding_percentage_capped_at_100",
    "label_f_register_change_allocation_based_on_schools_percent_of_formula",
    "label_g_teacher_salary_growth_2",
    "label_h_foundation_for_new_schools",
    "label_d_initial_fair_student_funding_allocations_total",
    "calculation_j_initial_fair_student_funding_allocations_total",
    "calculation_j_foundation",
    "label_w_final_school_fsf_percent",
    "calculation_j_fsf_formula_at_100",
    "as_of_date"
FROM "nyc-open-data-nbgq-j9jt"
