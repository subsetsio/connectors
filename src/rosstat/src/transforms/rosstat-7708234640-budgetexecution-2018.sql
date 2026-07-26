-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Наименование" AS column,
    "Раздел" AS column_2,
    "Подраздел" AS column_3,
    "Целевая статья расходов" AS column_4,
    "Вид расходов" AS column_5,
    "Утверждено бюджетной росписью (с учетом изменений) на 2018 год, тыс. рублей" AS "2018",
    "Кассовые расходы, тыс. рублей" AS column_6
FROM "rosstat-7708234640-budgetexecution-2018"
