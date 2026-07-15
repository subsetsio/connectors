-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Below65Years" AS total_below65years,
    "Total_65YearsandOver" AS total_65yearsandover,
    "LabourForce_Total_Total" AS labourforce_total_total,
    "LabourForce_Total_Below65Years" AS labourforce_total_below65years,
    "LabourForce_Total_65YearsandOver" AS labourforce_total_65yearsandover,
    "LabourForce_Employed_Total" AS labourforce_employed_total,
    "LabourForce_Employed_Below65Years" AS labourforce_employed_below65years,
    "LabourForce_Employed_65YearsandOver" AS labourforce_employed_65yearsandover,
    "LabourForce_Unemployed_Total" AS labourforce_unemployed_total,
    "LabourForce_Unemployed_Below65Years" AS labourforce_unemployed_below65years,
    "LabourForce_Unemployed_65YearsandOver" AS labourforce_unemployed_65yearsandover,
    "OutsidetheLabourForce_Total" AS outsidethelabourforce_total,
    "OutsidetheLabourForce_Below65Years" AS outsidethelabourforce_below65years,
    "OutsidetheLabourForce_65YearsandOver" AS outsidethelabourforce_65yearsandover
FROM "sg-data-d-11e9a7cc94f0011cad3fefeb59296b47"
