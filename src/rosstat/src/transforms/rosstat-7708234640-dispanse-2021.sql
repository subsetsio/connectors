-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Возраст" AS column,
    "Да" AS column_2,
    "Нет" AS column_3,
    "Отказ от ответа" AS column_4
FROM "rosstat-7708234640-dispanse-2021"
