-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("№ п/п" AS BIGINT) AS column,
    "Наименование" AS column_2,
    "Раздел" AS column_3,
    "Подраздел" AS column_4,
    "Целевая статья" AS column_5,
    "Вид расходов" AS column_6,
    "Утверждено бюджетной росписью (с учетом изменений) на 2017 год, тыс. рублей" AS "2017",
    "Кассовые расходы, тыс. рублей," AS column_7
FROM "rosstat-7708234640-budgetexecution2017"
