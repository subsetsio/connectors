-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "main_economic_activity_ar",
    "activity_code",
    "distribution_of_net_value_added_qr_000_operating_surp",
    "distribution_of_net_value_added_qr_000_compensation_" AS distribution_of_net_value_added_qr_000_compensation,
    "value_added_per_worker_qr",
    "productivity_of_employee_qr",
    "percentage_of_intermediate_services_to_output",
    "percentage_of_intermediate_goods_to_output",
    "average_annual_wage_1_qr"
FROM "qatar-planning-and-statistics-authority-main-economic-indicators-by-main-economic-activity-transport-and-communication-sector-activity-codes-4922-5229-isic-rev4"
