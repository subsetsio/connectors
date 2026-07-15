-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Permanent_Total" AS permanent_total,
    "Permanent_Males" AS permanent_males,
    "Permanent_Females" AS permanent_females,
    "Contract_Total" AS contract_total,
    "Contract_Males" AS contract_males,
    "Contract_Females" AS contract_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-8c432e951780543c0facf9049afb40cb"
