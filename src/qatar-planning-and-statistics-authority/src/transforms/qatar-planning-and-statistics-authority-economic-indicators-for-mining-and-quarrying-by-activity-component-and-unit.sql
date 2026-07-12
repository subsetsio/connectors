-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "main_economic_activity_ar",
    "distribution_of_net_value_added_value_qr_000_on_ope",
    "distribution_of_net_value_added_value_qr_000_on_co",
    "value_added_per_worker_qr",
    "productivity_of_employee_qr",
    "percentage_of_intermediate_services_to_output",
    "percentage_of_intermediate_goods_to_output",
    "average_annual_wage_1_qr"
FROM "qatar-planning-and-statistics-authority-economic-indicators-for-mining-and-quarrying-by-activity-component-and-unit"
