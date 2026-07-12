-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "establishments_by_number_of_employees",
    "v_a_per_employee_qr_nsyb_lmshtgl_mn_lqym_lmdf_ljmly",
    "productivity_per_employee_qr_ntjy_lmshtgl",
    "percentage_of_services_consumed_to_total_output_nsb_lmstlzmt_lkhdmy_l_qym_lntj",
    "percentage_of_goods_consumed_to_total_output_nsb_lmstlzmt_lsl_y_l_qym_lntj",
    "average_annual_wages_qr_mtwst_l_jr_lsnwy",
    "lmnshat_hsb_dd_lmshtglyn_hsb_hjm_lmnsh"
FROM "qatar-planning-and-statistics-authority-main-economic-indicators-of-transportation-and-communication-activity-by-size-of-establishment"
