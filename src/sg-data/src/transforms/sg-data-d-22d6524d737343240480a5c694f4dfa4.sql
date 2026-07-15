-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Owner" AS total_owner,
    "Total_Tenant" AS total_tenant,
    "Total_Others" AS total_others,
    "Single_Total" AS single_total,
    "Single_Owner" AS single_owner,
    "Single_Tenant" AS single_tenant,
    "Single_Others" AS single_others,
    "Married_Total" AS married_total,
    "Married_Owner" AS married_owner,
    "Married_Tenant" AS married_tenant,
    "Married_Others" AS married_others,
    "Widowed_Total" AS widowed_total,
    "Widowed_Owner" AS widowed_owner,
    "Widowed_Tenant" AS widowed_tenant,
    "Widowed_Others" AS widowed_others,
    "Divorced_Separated_Total" AS divorced_separated_total,
    "Divorced_Separated_Owner" AS divorced_separated_owner,
    "Divorced_Separated_Tenant" AS divorced_separated_tenant,
    "Divorced_Separated_Others" AS divorced_separated_others
FROM "sg-data-d-22d6524d737343240480a5c694f4dfa4"
