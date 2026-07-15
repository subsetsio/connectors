-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_None" AS total_none,
    "Total_1Child" AS total_1child,
    "Total_2Children" AS total_2children,
    "Total_3Children" AS total_3children,
    "Total_4Children" AS total_4children,
    "Total_5OrMoreChildren" AS total_5ormorechildren,
    "Chinese_Total" AS chinese_total,
    "Chinese_None" AS chinese_none,
    "Chinese_1Child" AS chinese_1child,
    "Chinese_2Children" AS chinese_2children,
    "Chinese_3Children" AS chinese_3children,
    "Chinese_4Children" AS chinese_4children,
    "Chinese_5OrMoreChildren" AS chinese_5ormorechildren,
    "Malays_Total" AS malays_total,
    "Malays_None" AS malays_none,
    "Malays_1Child" AS malays_1child,
    "Malays_2Children" AS malays_2children,
    "Malays_3Children" AS malays_3children,
    "Malays_4Children" AS malays_4children,
    "Malays_5OrMoreChildren" AS malays_5ormorechildren,
    "Indians_Total" AS indians_total,
    "Indians_None" AS indians_none,
    "Indians_1Child" AS indians_1child,
    "Indians_2Children" AS indians_2children,
    "Indians_3Children" AS indians_3children,
    "Indians_4Children" AS indians_4children,
    "Indians_5OrMoreChildren" AS indians_5ormorechildren,
    "Others_Total" AS others_total,
    "Others_None" AS others_none,
    "Others_1Child" AS others_1child,
    "Others_2Children" AS others_2children,
    "Others_3Children" AS others_3children,
    "Others_4Children" AS others_4children,
    "Others_5OrMoreChildren" AS others_5ormorechildren
FROM "sg-data-d-6ab43675ae3186635ac203d82ec13e9d"
