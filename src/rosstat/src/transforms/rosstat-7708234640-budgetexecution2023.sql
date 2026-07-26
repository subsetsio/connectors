-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Наименование" AS column,
    "Раздел" AS column_2,
    "Подраздел" AS column_3,
    "ГП" AS column_4,
    "Целевая статья расходов" AS column_5,
    "Вид расходов" AS column_6,
    "Утверждено бюджетной росписью (с учетом изменений) на 2023 год, тыс. рублей" AS "2023",
    "Кассовые расходы, тыс. рублей" AS column_7
FROM "rosstat-7708234640-budgetexecution2023"
