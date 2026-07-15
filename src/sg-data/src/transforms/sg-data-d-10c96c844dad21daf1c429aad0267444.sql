-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Employers_Total" AS employers_total,
    "Employers_Males" AS employers_males,
    "Employers_Females" AS employers_females,
    "OwnAccountWorkers_Total" AS ownaccountworkers_total,
    "OwnAccountWorkers_Males" AS ownaccountworkers_males,
    "OwnAccountWorkers_Females" AS ownaccountworkers_females,
    "Employees_Total" AS employees_total,
    "Employees_Males" AS employees_males,
    "Employees_Females" AS employees_females,
    "ContributingFamilyWorkers_Total" AS contributingfamilyworkers_total,
    "ContributingFamilyWorkers_Males" AS contributingfamilyworkers_males,
    "ContributingFamilyWorkers_Females" AS contributingfamilyworkers_females
FROM "sg-data-d-10c96c844dad21daf1c429aad0267444"
