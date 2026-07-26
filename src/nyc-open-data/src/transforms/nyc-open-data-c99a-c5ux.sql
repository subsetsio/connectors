-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "published_date",
    "project_id",
    "project_description",
    "budget_line",
    "budget_line_title",
    "asset_category",
    "greenhouse_gas_ghg_mitigation_tracking_category",
    "flood_resiliency_tracking_category",
    "heat_resiliency_tracking_category",
    "heat_vulnerability_index",
    "flood_vulnerability_index",
    "greenhouse_gas_ghg_mitigation",
    "flood_resiliency",
    "heat_resiliency",
    "environmental_and_social_benefits",
    "financial_plan",
    "fiscal_year",
    "fiscal_year_amount",
    "remarks"
FROM "nyc-open-data-c99a-c5ux"
