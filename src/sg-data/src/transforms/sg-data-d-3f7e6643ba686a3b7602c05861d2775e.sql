-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_NumberOfChildrenBorn_None" AS total_numberofchildrenborn_none,
    "Total_NumberOfChildrenBorn_1Child" AS total_numberofchildrenborn_1child,
    "Total_NumberOfChildrenBorn_2Children" AS total_numberofchildrenborn_2children,
    "Total_NumberOfChildrenBorn_3Children" AS total_numberofchildrenborn_3children,
    "Total_NumberOfChildrenBorn_4Children" AS total_numberofchildrenborn_4children,
    "Total_NumberOfChildrenBorn_5Children" AS total_numberofchildrenborn_5children,
    "Total_NumberOfChildrenBorn_6To7Children" AS total_numberofchildrenborn_6to7children,
    "Total_NumberOfChildrenBorn_8OrMoreChildren" AS total_numberofchildrenborn_8ormorechildren,
    "EconomicallyActive_Total" AS economicallyactive_total,
    "EconomicallyActive_NumberOfChildrenBorn_None" AS economicallyactive_numberofchildrenborn_none,
    "EconomicallyActive_NumberOfChildrenBorn_1Child" AS economicallyactive_numberofchildrenborn_1child,
    "EconomicallyActive_NumberOfChildrenBorn_2Children" AS economicallyactive_numberofchildrenborn_2children,
    "EconomicallyActive_NumberOfChildrenBorn_3Children" AS economicallyactive_numberofchildrenborn_3children,
    "EconomicallyActive_NumberOfChildrenBorn_4Children" AS economicallyactive_numberofchildrenborn_4children,
    "EconomicallyActive_NumberOfChildrenBorn_5Children" AS economicallyactive_numberofchildrenborn_5children,
    "EconomicallyActive_NumberOfChildrenBorn_6To7Children" AS economicallyactive_numberofchildrenborn_6to7children,
    "EconomicallyActive_NumberOfChildrenBorn_8OrMoreChildren" AS economicallyactive_numberofchildrenborn_8ormorechildren,
    "EconomicallyInactive_Total" AS economicallyinactive_total,
    "EconomicallyInactive_NumberOfChildrenBorn_None" AS economicallyinactive_numberofchildrenborn_none,
    "EconomicallyInactive_NumberOfChildrenBorn_1Child" AS economicallyinactive_numberofchildrenborn_1child,
    "EconomicallyInactive_NumberOfChildrenBorn_2Children" AS economicallyinactive_numberofchildrenborn_2children,
    "EconomicallyInactive_NumberOfChildrenBorn_3Children" AS economicallyinactive_numberofchildrenborn_3children,
    "EconomicallyInactive_NumberOfChildrenBorn_4Children" AS economicallyinactive_numberofchildrenborn_4children,
    "EconomicallyInactive_NumberOfChildrenBorn_5Children" AS economicallyinactive_numberofchildrenborn_5children,
    "EconomicallyInactive_NumberOfChildrenBorn_6To7Children" AS economicallyinactive_numberofchildrenborn_6to7children,
    "EconomicallyInactive_NumberOfChildrenBorn_8OrMoreChildren" AS economicallyinactive_numberofchildrenborn_8ormorechildren
FROM "sg-data-d-3f7e6643ba686a3b7602c05861d2775e"
