-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "№ п/п" AS column,
    CAST("№  нормативного правового акта" AS BIGINT) AS column_2,
    "Вид и дата издания нормативного правового акта" AS column_3,
    "Наименование нормативного правового акта" AS column_4,
    "Информация о регистрации в Министерстве юстиции Российской Федерации" AS column_5
FROM "rosstat-7708234640-listnormativeacts2022"
