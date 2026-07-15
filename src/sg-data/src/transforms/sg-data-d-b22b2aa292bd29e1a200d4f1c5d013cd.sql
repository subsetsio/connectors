-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_None" AS total_none,
    "Total_1Child" AS total_1child,
    "Total_2Children" AS total_2children,
    "Total_3Children" AS total_3children,
    "Total_4Children" AS total_4children,
    "Total_5OrMoreChildren" AS total_5ormorechildren,
    "EconomicallyActive_Total" AS economicallyactive_total,
    "EconomicallyActive_None" AS economicallyactive_none,
    "EconomicallyActive_1Child" AS economicallyactive_1child,
    "EconomicallyActive_2Children" AS economicallyactive_2children,
    "EconomicallyActive_3Children" AS economicallyactive_3children,
    "EconomicallyActive_4Children" AS economicallyactive_4children,
    "EconomicallyActive_5OrMoreChildren" AS economicallyactive_5ormorechildren,
    "EconomicallyInactive_Total" AS economicallyinactive_total,
    "EconomicallyInactive_None" AS economicallyinactive_none,
    "EconomicallyInactive_1Child" AS economicallyinactive_1child,
    "EconomicallyInactive_2Children" AS economicallyinactive_2children,
    "EconomicallyInactive_3Children" AS economicallyinactive_3children,
    "EconomicallyInactive_4Children" AS economicallyinactive_4children,
    "EconomicallyInactive_5OrMoreChildren" AS economicallyinactive_5ormorechildren
FROM "sg-data-d-b22b2aa292bd29e1a200d4f1c5d013cd"
