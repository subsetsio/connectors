-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total_Total" AS total_total,
    "Total_NumberOfChildrenBorn_None" AS total_numberofchildrenborn_none,
    "Total_NumberOfChildrenBorn_1Child" AS total_numberofchildrenborn_1child,
    "Total_NumberOfChildrenBorn_2Children" AS total_numberofchildrenborn_2children,
    "Total_NumberOfChildrenBorn_3Children" AS total_numberofchildrenborn_3children,
    "Total_NumberOfChildrenBorn_4Children" AS total_numberofchildrenborn_4children,
    "Total_NumberOfChildrenBorn_5OrMoreChildren" AS total_numberofchildrenborn_5ormorechildren,
    "EconomicallyActive_Total" AS economicallyactive_total,
    "EconomicallyActive_NumberOfChildrenBorn_None" AS economicallyactive_numberofchildrenborn_none,
    "EconomicallyActive_NumberOfChildrenBorn_1Child" AS economicallyactive_numberofchildrenborn_1child,
    "EconomicallyActive_NumberOfChildrenBorn_2Children" AS economicallyactive_numberofchildrenborn_2children,
    "EconomicallyActive_NumberOfChildrenBorn_3Children" AS economicallyactive_numberofchildrenborn_3children,
    "EconomicallyActive_NumberOfChildrenBorn_4Children" AS economicallyactive_numberofchildrenborn_4children,
    "EconomicallyActive_NumberOfChildrenBorn_5OrMoreChildren" AS economicallyactive_numberofchildrenborn_5ormorechildren,
    "EconomicallyInactive_Total" AS economicallyinactive_total,
    "EconomicallyInactive_NumberOfChildrenBorn_None" AS economicallyinactive_numberofchildrenborn_none,
    "EconomicallyInactive_NumberOfChildrenBorn_1Child" AS economicallyinactive_numberofchildrenborn_1child,
    "EconomicallyInactive_NumberOfChildrenBorn_2Children" AS economicallyinactive_numberofchildrenborn_2children,
    "EconomicallyInactive_NumberOfChildrenBorn_3Children" AS economicallyinactive_numberofchildrenborn_3children,
    "EconomicallyInactive_NumberOfChildrenBorn_4Children" AS economicallyinactive_numberofchildrenborn_4children,
    "EconomicallyInactive_NumberOfChildrenBorn_5OrMoreChildren" AS economicallyinactive_numberofchildrenborn_5ormorechildren
FROM "sg-data-d-ab7c03bf5099a68379e99eaaa5543402"
