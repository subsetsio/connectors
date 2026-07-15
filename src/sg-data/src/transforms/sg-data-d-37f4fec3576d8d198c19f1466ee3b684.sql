-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "LabourForce_Total_Total" AS labourforce_total_total,
    "LabourForce_Total_Males" AS labourforce_total_males,
    "LabourForce_Total_Females" AS labourforce_total_females,
    "LabourForce_Employed_Total" AS labourforce_employed_total,
    "LabourForce_Employed_Males" AS labourforce_employed_males,
    "LabourForce_Employed_Females" AS labourforce_employed_females,
    "LabourForce_Unemployed_Total" AS labourforce_unemployed_total,
    "LabourForce_Unemployed_Males" AS labourforce_unemployed_males,
    "LabourForce_Unemployed_Females" AS labourforce_unemployed_females,
    "OutsidetheLabourForce_Total" AS outsidethelabourforce_total,
    "OutsidetheLabourForce_Males" AS outsidethelabourforce_males,
    "OutsidetheLabourForce_Females" AS outsidethelabourforce_females
FROM "sg-data-d-37f4fec3576d8d198c19f1466ee3b684"
