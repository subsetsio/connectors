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
    "Beneficiary_Group" AS beneficiary_group,
    "Cost_Sharing_Support" AS cost_sharing_support,
    "Projected_Spending_2026" AS projected_spending_2026,
    "Actual_Spending_2026" AS actual_spending_2026
FROM "cms-522f7e2d-58fc-4267-a073-8fa5fd18859f"
