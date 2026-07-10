-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "ACO_ID" AS aco_id,
    "ACO_Name" AS aco_name,
    "Payment_Use" AS payment_use,
    "General_Spend_Category" AS general_spend_category,
    "General_Spend_Subcategory" AS general_spend_subcategory,
    "Total_AIP_Funding_Received_through_December_2025" AS total_aip_funding_received_through_december_2025,
    "Projected_Spending_2024" AS projected_spending_2024,
    "Actual_Spending_2024" AS actual_spending_2024,
    "Projected_Spending_2025" AS projected_spending_2025,
    "Actual_Spending_2025" AS actual_spending_2025,
    "Projected_Spending_2026" AS projected_spending_2026,
    "Actual_Spending_2026" AS actual_spending_2026
FROM "cms-a3d35ba1-3ff4-48dd-91b4-8e1f9e7a19b7"
