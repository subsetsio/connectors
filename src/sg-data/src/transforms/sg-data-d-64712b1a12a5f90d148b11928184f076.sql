-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_NumberofChildrenBorn_None" AS total_numberofchildrenborn_none,
    "Total_NumberofChildrenBorn_1Child" AS total_numberofchildrenborn_1child,
    "Total_NumberofChildrenBorn_2Children" AS total_numberofchildrenborn_2children,
    "Total_NumberofChildrenBorn_3Children" AS total_numberofchildrenborn_3children,
    "Total_NumberofChildrenBorn_4Children" AS total_numberofchildrenborn_4children,
    "Total_NumberofChildrenBorn_5orMoreChildren" AS total_numberofchildrenborn_5ormorechildren,
    "Chinese_Total" AS chinese_total,
    "Chinese_NumberofChildrenBorn_None" AS chinese_numberofchildrenborn_none,
    "Chinese_NumberofChildrenBorn_1Child" AS chinese_numberofchildrenborn_1child,
    "Chinese_NumberofChildrenBorn_2Children" AS chinese_numberofchildrenborn_2children,
    "Chinese_NumberofChildrenBorn_3Children" AS chinese_numberofchildrenborn_3children,
    "Chinese_NumberofChildrenBorn_4Children" AS chinese_numberofchildrenborn_4children,
    "Chinese_NumberofChildrenBorn_5Children" AS chinese_numberofchildrenborn_5children,
    "Malays_Total" AS malays_total,
    "Malays_NumberofChildrenBorn_None" AS malays_numberofchildrenborn_none,
    "Malays_NumberofChildrenBorn_1Child" AS malays_numberofchildrenborn_1child,
    "Malays_NumberofChildrenBorn_2Children" AS malays_numberofchildrenborn_2children,
    "Malays_NumberofChildrenBorn_3Children" AS malays_numberofchildrenborn_3children,
    "Malays_NumberofChildrenBorn_4Children" AS malays_numberofchildrenborn_4children,
    "Malays_NumberofChildrenBorn_5Children" AS malays_numberofchildrenborn_5children,
    "Indians_Total" AS indians_total,
    "Indians_NumberofChildrenBorn_None" AS indians_numberofchildrenborn_none,
    "Indians_NumberofChildrenBorn_1Child" AS indians_numberofchildrenborn_1child,
    "Indians_NumberofChildrenBorn_2Children" AS indians_numberofchildrenborn_2children,
    "Indians_NumberofChildrenBorn_3Children" AS indians_numberofchildrenborn_3children,
    "Indians_NumberofChildrenBorn_4Children" AS indians_numberofchildrenborn_4children,
    "Indians_NumberofChildrenBorn_5Children" AS indians_numberofchildrenborn_5children,
    "Others_Total" AS others_total,
    "Others_NumberofChildrenBorn_None" AS others_numberofchildrenborn_none,
    "Others_NumberofChildrenBorn_1Child" AS others_numberofchildrenborn_1child,
    "Others_NumberofChildrenBorn_2Children" AS others_numberofchildrenborn_2children,
    "Others_NumberofChildrenBorn_3Children" AS others_numberofchildrenborn_3children,
    "Others_NumberofChildrenBorn_4Children" AS others_numberofchildrenborn_4children,
    "Others_NumberofChildrenBorn_5Children" AS others_numberofchildrenborn_5children
FROM "sg-data-d-64712b1a12a5f90d148b11928184f076"
