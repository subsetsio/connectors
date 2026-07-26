-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "fundind_source_name",
    "fps_group",
    "fps_group_name",
    "agency_number",
    "agency_name",
    "revenue_category",
    "revenue_category_name",
    "revenue_class_code",
    "revenue_class_name",
    "budget_code",
    "revenue_source",
    "revenue_source_name",
    "revenue_structure_description",
    "adopted_budget_amount",
    "current_modified_budget_amount",
    "yr1_fy",
    "year_1_revenue_amount",
    "year_2_revenue_amount",
    "year_3_revenue_amount",
    "year_4_revenue_amount",
    "year_5_revenue_amount"
FROM "nyc-open-data-ugzk-a6x4"
