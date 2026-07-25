-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Возраст" AS column,
    "Очень хорошее" AS column_2,
    "Хорошее" AS column_3,
    "Удовлетворительное" AS column_4,
    "Плохое" AS column_5,
    "Очень плохое" AS column_6,
    "Затрудняюсь ответить" AS column_7
FROM "rosstat-7708234640-healthage-2021"
