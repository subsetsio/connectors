-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    "№ п/п" AS column,
    "Статистический показатель по национальному проекту" AS column_2,
    "Ссылка на показатель в ЕМИСС" AS column_3,
    "Пункт ФПСР" AS column_4,
    "Сроки публикации (в соответствии с ФПСР)" AS column_5,
    "Ответственный исполнитель (ФИО, телефон)" AS column_6
FROM "rosstat-7708234640-nationalprojects"
