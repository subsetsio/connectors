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
    "Chinese_Total" AS chinese_total,
    "Chinese_Owner" AS chinese_owner,
    "Chinese_Tenant" AS chinese_tenant,
    "Chinese_Others" AS chinese_others,
    "Malays_Total" AS malays_total,
    "Malays_Owner" AS malays_owner,
    "Malays_Tenant" AS malays_tenant,
    "Malays_Others" AS malays_others,
    "Indians_Total" AS indians_total,
    "Indians_Owner" AS indians_owner,
    "Indians_Tenant" AS indians_tenant,
    "Indians_Others" AS indians_others,
    "Others_Total" AS others_total,
    "Others_Owner" AS others_owner,
    "Others_Tenant" AS others_tenant,
    "Others_Others" AS others_others
FROM "sg-data-d-db508815adc112fc474dc9d1871d82f7"
