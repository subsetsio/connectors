-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Возраст" AS column,
    "Да, и я пользуюсь ими" AS column_2,
    "Да, но они для меня недоступны" AS column_3,
    "Да, но я не пользуюсь ими" AS column_4,
    "Нет" AS column_5,
    "Затрудняюсь ответить" AS column_6,
    "Отказ от ответа" AS column_7
FROM "rosstat-7708234640-placesforsports-2021"
