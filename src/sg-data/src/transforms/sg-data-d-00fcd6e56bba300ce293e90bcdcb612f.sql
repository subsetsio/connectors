-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Owner" AS total_owner,
    "Total_Tenant" AS total_tenant,
    "Total_Others" AS total_others,
    "1Person_Total" AS 1person_total,
    "1Person_Owner" AS 1person_owner,
    "1Person_Tenant" AS 1person_tenant,
    "1Person_Others" AS 1person_others,
    "2Persons_Total" AS 2persons_total,
    "2Persons_Owner" AS 2persons_owner,
    "2Persons_Tenant" AS 2persons_tenant,
    "2Persons_Others" AS 2persons_others,
    "3Persons_Total" AS 3persons_total,
    "3Persons_Owner" AS 3persons_owner,
    "3Persons_Tenant" AS 3persons_tenant,
    "3Persons_Others" AS 3persons_others,
    "4Persons_Total" AS 4persons_total,
    "4Persons_Owner" AS 4persons_owner,
    "4Persons_Tenant" AS 4persons_tenant,
    "4Persons_Others" AS 4persons_others,
    "5Persons_Total" AS 5persons_total,
    "5Persons_Owner" AS 5persons_owner,
    "5Persons_Tenant" AS 5persons_tenant,
    "5Persons_Others" AS 5persons_others,
    "6OrMorePersons_Total" AS 6ormorepersons_total,
    "6OrMorePersons_Owner" AS 6ormorepersons_owner,
    "6OrMorePersons_Tenant" AS 6ormorepersons_tenant,
    "6OrMorePersons_Others" AS 6ormorepersons_others
FROM "sg-data-d-00fcd6e56bba300ce293e90bcdcb612f"
