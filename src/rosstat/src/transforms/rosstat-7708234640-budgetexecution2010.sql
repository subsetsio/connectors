-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("№ п/п" AS BIGINT) AS column,
    "Наименование" AS column_2,
    "Раздел, подраздел" AS column_3,
    "Целевая статья расходов" AS column_4,
    "Утверждено бюджетной росписью (с учетом изменений) на год, тыс. руб." AS column_5,
    "Кассовые расходы, тыс. руб." AS column_6
FROM "rosstat-7708234640-budgetexecution2010"
