-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "activity_code_rmz_lnsht",
    "main_economic_activity",
    "operating_surplus_value_in_1_000_qr_fy_d_ltshgyl_lqym_b_lf_ryl_qtry",
    "compensation_of_employees_value_in_1_000_qr_t_wydt_l_mlyn_lqym_b_lf_ryl_qtry",
    "value_added_per_worker_qr_nsyb_lmshtgl_mn_lqym_lmdf_ljmly_lryl_lqtry",
    "productivity_of_employee_qr_ntjy_lmshtgl_lryl_lqtry",
    "percentage_of_intermediate_services_to_output_nsb_lmstlzmt_lkhdmy_l_qym_lntj",
    "percentage_of_intermediate_goods_to_output_nsb_lmstlzmt_lsl_y_l_qym_lntj",
    "average_annual_wage_qr_mtwst_l_jr_lsnwy_lryl_lqtry",
    "lnsht_lqtsdy_lry_ysy"
FROM "qatar-planning-and-statistics-authority-hotels-and-restaurants-statistics-economic-indicators-in-hotels-and-restaurants-by-activity0"
