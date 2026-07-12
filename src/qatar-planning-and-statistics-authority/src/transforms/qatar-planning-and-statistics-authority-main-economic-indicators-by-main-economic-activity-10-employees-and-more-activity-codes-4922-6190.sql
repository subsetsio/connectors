-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "average_annual_wage_1_qr",
    "percentage_of_intermediate_goods_to_output",
    "percentage_of_intermediate_services_to_output",
    "productivity_of_employee_qr",
    "value_added_per_worker_qr_nsyb_lmshtgl_mn_lqym_lmdf_ljmly_ryl_qtry",
    "compensation_of_employees_qr",
    "operating_surplus",
    "main_economic_activity_ar"
FROM "qatar-planning-and-statistics-authority-main-economic-indicators-by-main-economic-activity-10-employees-and-more-activity-codes-4922-6190"
