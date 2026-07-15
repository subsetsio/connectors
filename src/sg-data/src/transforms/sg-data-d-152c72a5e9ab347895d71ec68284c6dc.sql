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
    "SingaporeCitizens_Total" AS singaporecitizens_total,
    "SingaporeCitizens_NumberofChildrenBorn_None" AS singaporecitizens_numberofchildrenborn_none,
    "SingaporeCitizens_NumberofChildrenBorn_1Child" AS singaporecitizens_numberofchildrenborn_1child,
    "SingaporeCitizens_NumberofChildrenBorn_2Children" AS singaporecitizens_numberofchildrenborn_2children,
    "SingaporeCitizens_NumberofChildrenBorn_3Children" AS singaporecitizens_numberofchildrenborn_3children,
    "SingaporeCitizens_NumberofChildrenBorn_4Children" AS singaporecitizens_numberofchildrenborn_4children,
    "SingaporeCitizens_NumberofChildrenBorn_5orMoreChildren" AS singaporecitizens_numberofchildrenborn_5ormorechildren,
    "PermanentResidents_Total" AS permanentresidents_total,
    "PermanentResidents_NumberofChildrenBorn_None" AS permanentresidents_numberofchildrenborn_none,
    "PermanentResidents_NumberofChildrenBorn_1Child" AS permanentresidents_numberofchildrenborn_1child,
    "PermanentResidents_NumberofChildrenBorn_2Children" AS permanentresidents_numberofchildrenborn_2children,
    "PermanentResidents_NumberofChildrenBorn_3Children" AS permanentresidents_numberofchildrenborn_3children,
    "PermanentResidents_NumberofChildrenBorn_4Children" AS permanentresidents_numberofchildrenborn_4children,
    "PermanentResidents_NumberofChildrenBorn_5orMoreChildren" AS permanentresidents_numberofchildrenborn_5ormorechildren
FROM "sg-data-d-152c72a5e9ab347895d71ec68284c6dc"
