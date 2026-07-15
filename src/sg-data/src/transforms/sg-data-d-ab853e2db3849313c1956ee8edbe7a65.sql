-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "EconomicallyActive_Total_Total" AS economicallyactive_total_total,
    "EconomicallyActive_Total_Males" AS economicallyactive_total_males,
    "EconomicallyActive_Total_Females" AS economicallyactive_total_females,
    "EconomicallyActive_Working_Total" AS economicallyactive_working_total,
    "EconomicallyActive_Working_Males" AS economicallyactive_working_males,
    "EconomicallyActive_Working_Females" AS economicallyactive_working_females,
    "EconomicallyActive_Unemployed_Total" AS economicallyactive_unemployed_total,
    "EconomicallyActive_Unemployed_Males" AS economicallyactive_unemployed_males,
    "EconomicallyActive_Unemployed_Females" AS economicallyactive_unemployed_females,
    "EconomicallyInactive_Total" AS economicallyinactive_total,
    "EconomicallyInactive_Males" AS economicallyinactive_males,
    "EconomicallyInactive_Females" AS economicallyinactive_females
FROM "sg-data-d-ab853e2db3849313c1956ee8edbe7a65"
