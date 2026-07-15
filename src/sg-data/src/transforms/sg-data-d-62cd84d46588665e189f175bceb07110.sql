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
    "SingaporeCitizens_Total" AS singaporecitizens_total,
    "SingaporeCitizens_NumberOfChildrenBorn_None" AS singaporecitizens_numberofchildrenborn_none,
    "SingaporeCitizens_NumberOfChildrenBorn_1Child" AS singaporecitizens_numberofchildrenborn_1child,
    "SingaporeCitizens_NumberOfChildrenBorn_2Children" AS singaporecitizens_numberofchildrenborn_2children,
    "SingaporeCitizens_NumberOfChildrenBorn_3Children" AS singaporecitizens_numberofchildrenborn_3children,
    "SingaporeCitizens_NumberOfChildrenBorn_4Children" AS singaporecitizens_numberofchildrenborn_4children,
    "SingaporeCitizens_NumberOfChildrenBorn_5Children" AS singaporecitizens_numberofchildrenborn_5children,
    "SingaporeCitizens_NumberOfChildrenBorn_6To7Children" AS singaporecitizens_numberofchildrenborn_6to7children,
    "SingaporeCitizens_NumberOfChildrenBorn_8OrMoreChildren" AS singaporecitizens_numberofchildrenborn_8ormorechildren,
    "PermanentResidents_Total" AS permanentresidents_total,
    "PermanentResidents_NumberOfChildrenBorn_None" AS permanentresidents_numberofchildrenborn_none,
    "PermanentResidents_NumberOfChildrenBorn_1Child" AS permanentresidents_numberofchildrenborn_1child,
    "PermanentResidents_NumberOfChildrenBorn_2Children" AS permanentresidents_numberofchildrenborn_2children,
    "PermanentResidents_NumberOfChildrenBorn_3Children" AS permanentresidents_numberofchildrenborn_3children,
    "PermanentResidents_NumberOfChildrenBorn_4Children" AS permanentresidents_numberofchildrenborn_4children,
    "PermanentResidents_NumberOfChildrenBorn_5Children" AS permanentresidents_numberofchildrenborn_5children,
    "PermanentResidents_NumberOfChildrenBorn_6To7Children" AS permanentresidents_numberofchildrenborn_6to7children,
    "PermanentResidents_NumberOfChildrenBorn_8OrMoreChildren" AS permanentresidents_numberofchildrenborn_8ormorechildren
FROM "sg-data-d-62cd84d46588665e189f175bceb07110"
