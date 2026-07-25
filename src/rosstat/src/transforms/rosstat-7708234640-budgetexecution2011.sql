-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "№ п/п" AS column,
    "Наименование расхода" AS column_2,
    "Код расхода по БК" AS column_3,
    "Утверждено бюджетной росписью (с учетом изменений на год), тыс.руб." AS column_4,
    "Кассовые расходы, тыс. руб." AS column_5
FROM "rosstat-7708234640-budgetexecution2011"
