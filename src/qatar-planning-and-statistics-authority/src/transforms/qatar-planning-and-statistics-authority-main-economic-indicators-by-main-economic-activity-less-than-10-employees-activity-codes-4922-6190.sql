-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "average_annual_wage_1_qr_mtwst_l_jr_lsnwy_1_ryl_qtry",
    "percentage_of_intermediate_goods_to_output_nsb_qym_lmstlzmt_lsl_y_l_qym_lntj",
    "percentage_of_intermediate_services_to_output_nsb_qym_lmstlzmt_lkhdmy_l_qym_lntj",
    "productivity_of_employee_qr_ntjy_lmshtgl_ryl_qtry",
    "value_added_per_worker_qr_nsyb_lmshtgl_mn_lqym_lmdf_ljmly_ryl_qtry",
    "compensation_of_employees_t_wydt_l_mlyn_qr",
    "operating_surplus_fy_d_ltshgyl_qr",
    "main_economic_activity_ar"
FROM "qatar-planning-and-statistics-authority-main-economic-indicators-by-main-economic-activity-less-than-10-employees-activity-codes-4922-6190"
