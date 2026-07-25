-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Возраст" AS column,
    "Да, ежедневно" AS column_2,
    "Не каждый день (периодически)" AS column_3,
    "Нет, совсем не курю" AS column_4,
    "Отказ от ответа" AS column_5
FROM "rosstat-7708234640-smokingnow-2021"
