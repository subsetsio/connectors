-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Chinese" AS total_chinese,
    "Total_Malays" AS total_malays,
    "Total_Indians" AS total_indians,
    "Total_Others" AS total_others,
    "LabourForce_Total" AS labourforce_total,
    "LabourForce_Chinese" AS labourforce_chinese,
    "LabourForce_Malays" AS labourforce_malays,
    "LabourForce_Indians" AS labourforce_indians,
    "LabourForce_Others" AS labourforce_others,
    "OutsidetheLabourForce_Total" AS outsidethelabourforce_total,
    "OutsidetheLabourForce_Chinese" AS outsidethelabourforce_chinese,
    "OutsidetheLabourForce_Malays" AS outsidethelabourforce_malays,
    "OutsidetheLabourForce_Indians" AS outsidethelabourforce_indians,
    "OutsidetheLabourForce_Others" AS outsidethelabourforce_others
FROM "sg-data-d-6ce6cea5acfe2fdc0cc64d23a24b376e"
