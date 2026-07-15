-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_NumberofChildrenBorn_None" AS total_numberofchildrenborn_none,
    "Total_NumberofChildrenBorn_1Child" AS total_numberofchildrenborn_1child,
    "Total_NumberofChildrenBorn_2Children" AS total_numberofchildrenborn_2children,
    "Total_NumberofChildrenBorn_3Children" AS total_numberofchildrenborn_3children,
    "Total_NumberofChildrenBorn_4Children" AS total_numberofchildrenborn_4children,
    "Total_NumberofChildrenBorn_5orMoreChildren" AS total_numberofchildrenborn_5ormorechildren,
    "LabourForce_Total" AS labourforce_total,
    "LabourForce_NumberofChildrenBorn_None" AS labourforce_numberofchildrenborn_none,
    "LabourForce_NumberofChildrenBorn_1Child" AS labourforce_numberofchildrenborn_1child,
    "LabourForce_NumberofChildrenBorn_2Children" AS labourforce_numberofchildrenborn_2children,
    "LabourForce_NumberofChildrenBorn_3Children" AS labourforce_numberofchildrenborn_3children,
    "LabourForce_NumberofChildrenBorn_4Children" AS labourforce_numberofchildrenborn_4children,
    "LabourForce_NumberofChildrenBorn_5orMoreChildren" AS labourforce_numberofchildrenborn_5ormorechildren,
    "OutsidetheLabourForce_Total" AS outsidethelabourforce_total,
    "OutsidetheLabourForce_NumberofChildrenBorn_None" AS outsidethelabourforce_numberofchildrenborn_none,
    "OutsidetheLabourForce_NumberofChildrenBorn_1Child" AS outsidethelabourforce_numberofchildrenborn_1child,
    "OutsidetheLabourForce_NumberofChildrenBorn_2Children" AS outsidethelabourforce_numberofchildrenborn_2children,
    "OutsidetheLabourForce_NumberofChildrenBorn_3Children" AS outsidethelabourforce_numberofchildrenborn_3children,
    "OutsidetheLabourForce_NumberofChildrenBorn_4Children" AS outsidethelabourforce_numberofchildrenborn_4children,
    "OutsidetheLabourForce_NumberofChildrenBorn_5orMoreChildren" AS outsidethelabourforce_numberofchildrenborn_5ormorechildren
FROM "sg-data-d-247c66edbfe81aaca0b639e7634117e5"
