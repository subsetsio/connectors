-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Thousands" AS thousands,
    "Total_Total" AS total_total,
    "Total_1Person" AS total_1person,
    "Total_2Persons" AS total_2persons,
    "Total_3Persons" AS total_3persons,
    "Total_4Persons" AS total_4persons,
    "Total_5Persons" AS total_5persons,
    "Total_6OrMorePersons" AS total_6ormorepersons,
    "Chinese_Total" AS chinese_total,
    "Chinese_1Person" AS chinese_1person,
    "Chinese_2Persons" AS chinese_2persons,
    "Chinese_3Persons" AS chinese_3persons,
    "Chinese_4Persons" AS chinese_4persons,
    "Chinese_5Persons" AS chinese_5persons,
    "Chinese_6OrMorePersons" AS chinese_6ormorepersons,
    "Malays_Total" AS malays_total,
    "Malays_1Person" AS malays_1person,
    "Malays_2Persons" AS malays_2persons,
    "Malays_3Persons" AS malays_3persons,
    "Malays_4Persons" AS malays_4persons,
    "Malays_5Persons" AS malays_5persons,
    "Malays_6OrMorePersons" AS malays_6ormorepersons,
    "Indians_Total" AS indians_total,
    "Indians_1Person" AS indians_1person,
    "Indians_2Persons" AS indians_2persons,
    "Indians_3Persons" AS indians_3persons,
    "Indians_4Persons" AS indians_4persons,
    "Indians_5Persons" AS indians_5persons,
    "Indians_6OrMorePersons" AS indians_6ormorepersons,
    "Others_Total" AS others_total,
    "Others_1Person" AS others_1person,
    "Others_2Persons" AS others_2persons,
    "Others_3Persons" AS others_3persons,
    "Others_4Persons" AS others_4persons,
    "Others_5Persons" AS others_5persons,
    "Others_6OrMorePersons" AS others_6ormorepersons
FROM "sg-data-d-1e5429ac896a0dfccecf007a8a03a646"
