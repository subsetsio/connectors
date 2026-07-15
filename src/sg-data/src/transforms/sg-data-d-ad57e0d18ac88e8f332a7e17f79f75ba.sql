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
    "UnpaidFamilyWorkers_Total" AS unpaidfamilyworkers_total,
    "UnpaidFamilyWorkers_Males" AS unpaidfamilyworkers_males,
    "UnpaidFamilyWorkers_Females" AS unpaidfamilyworkers_females
FROM "sg-data-d-ad57e0d18ac88e8f332a7e17f79f75ba"
