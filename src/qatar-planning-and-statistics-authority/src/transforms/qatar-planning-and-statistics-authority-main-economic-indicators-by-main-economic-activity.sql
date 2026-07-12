-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "lnsht_lqtsd_lry_ysy",
    "distribution_of_net_value_added_value_qr_000_on_operating_surplus",
    "distribution_of_net_value_added_value_qr_000_on_compensation_of_employees",
    "value_added_per_worker_qr",
    "productivity_of_employee_qr",
    "percentage_of_intermediate_services_to_output",
    "percentage_of_intermediate_goods_to_output",
    "average_annual_wage_qr"
FROM "qatar-planning-and-statistics-authority-main-economic-indicators-by-main-economic-activity"
