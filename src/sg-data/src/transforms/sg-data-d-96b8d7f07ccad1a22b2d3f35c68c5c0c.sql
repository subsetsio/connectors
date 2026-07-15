-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Thousands" AS thousands,
    "Total_Total" AS total_total,
    "Total_NumberOfChildrenBorn_None" AS total_numberofchildrenborn_none,
    "Total_NumberOfChildrenBorn_1Child" AS total_numberofchildrenborn_1child,
    "Total_NumberOfChildrenBorn_2Children" AS total_numberofchildrenborn_2children,
    "Total_NumberOfChildrenBorn_3Children" AS total_numberofchildrenborn_3children,
    "Total_NumberOfChildrenBorn_4Children" AS total_numberofchildrenborn_4children,
    "Total_NumberOfChildrenBorn_5OrMoreChildren" AS total_numberofchildrenborn_5ormorechildren,
    "Chinese_Total" AS chinese_total,
    "Chinese_NumberOfChildrenBorn_None" AS chinese_numberofchildrenborn_none,
    "Chinese_NumberOfChildrenBorn_1Child" AS chinese_numberofchildrenborn_1child,
    "Chinese_NumberOfChildrenBorn_2Children" AS chinese_numberofchildrenborn_2children,
    "Chinese_NumberOfChildrenBorn_3Children" AS chinese_numberofchildrenborn_3children,
    "Chinese_NumberOfChildrenBorn_4Children" AS chinese_numberofchildrenborn_4children,
    "Chinese_NumberOfChildrenBorn_5OrMoreChildren" AS chinese_numberofchildrenborn_5ormorechildren,
    "Malays_Total" AS malays_total,
    "Malays_NumberOfChildrenBorn_None" AS malays_numberofchildrenborn_none,
    "Malays_NumberOfChildrenBorn_1Child" AS malays_numberofchildrenborn_1child,
    "Malays_NumberOfChildrenBorn_2Children" AS malays_numberofchildrenborn_2children,
    "Malays_NumberOfChildrenBorn_3Children" AS malays_numberofchildrenborn_3children,
    "Malays_NumberOfChildrenBorn_4Children" AS malays_numberofchildrenborn_4children,
    "Malays_NumberOfChildrenBorn_5OrMoreChildren" AS malays_numberofchildrenborn_5ormorechildren,
    "Indians_Total" AS indians_total,
    "Indians_NumberOfChildrenBorn_None" AS indians_numberofchildrenborn_none,
    "Indians_NumberOfChildrenBorn_1Child" AS indians_numberofchildrenborn_1child,
    "Indians_NumberOfChildrenBorn_2Children" AS indians_numberofchildrenborn_2children,
    "Indians_NumberOfChildrenBorn_3Children" AS indians_numberofchildrenborn_3children,
    "Indians_NumberOfChildrenBorn_4Children" AS indians_numberofchildrenborn_4children,
    "Indians_NumberOfChildrenBorn_5OrMoreChildren" AS indians_numberofchildrenborn_5ormorechildren,
    "Others_Total" AS others_total,
    "Others_NumberOfChildrenBorn_None" AS others_numberofchildrenborn_none,
    "Others_NumberOfChildrenBorn_1Child" AS others_numberofchildrenborn_1child,
    "Others_NumberOfChildrenBorn_2Children" AS others_numberofchildrenborn_2children,
    "Others_NumberOfChildrenBorn_3Children" AS others_numberofchildrenborn_3children,
    "Others_NumberOfChildrenBorn_4Children" AS others_numberofchildrenborn_4children,
    "Others_NumberOfChildrenBorn_5OrMoreChildren" AS others_numberofchildrenborn_5ormorechildren
FROM "sg-data-d-96b8d7f07ccad1a22b2d3f35c68c5c0c"
