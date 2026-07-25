-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    "№ п/п" AS column,
    "Наименование подпрограммы, ВЦП, основного мероприятия, мероприятия ФЦП, контрольного события программы" AS column_2,
    "Статус" AS column_3,
    "Ответственный исполнитель (Ф.И.О., должность, организация)" AS column_4,
    "Ожидаемый результат реализации мероприятия" AS column_5,
    "Срок начала реализации" AS column_6,
    "Срок окончания реализации (дата контрольного события)" AS column_7,
    "Код бюджетной классификации" AS column_8,
    "Объем ресурсного обеспечения, тыс. руб." AS column_9
FROM "rosstat-7708234640-stateprogram"
