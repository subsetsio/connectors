-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "State" AS state,
    "County" AS county,
    "MCO Name" AS mco_name,
    "Service Category" AS service_category,
    "Number of Active Patients" AS number_of_active_patients,
    "Number of Eligible MCO Patients" AS number_of_eligible_mco_patients,
    CAST("Number of Providers" AS BIGINT) AS number_of_providers,
    "Percent Of Eligible Patients Receiving Services" AS percent_of_eligible_patients_receiving_services,
    "Number of Services per Active Patient" AS number_of_services_per_active_patient,
    "Number of Active Patients per Provider" AS number_of_active_patients_per_provider,
    CAST("Calendar Year" AS BIGINT) AS calendar_year,
    "Plan Category" AS plan_category
FROM "cms-a93f5362-2fe6-4b4d-8260-118be0d618e0"
