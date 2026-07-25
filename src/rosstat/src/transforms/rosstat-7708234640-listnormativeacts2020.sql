-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "№ п/п" AS column,
    "Наименование нормативного правового акта" AS column_2,
    "Дата и номер регистрации в Министерстве юстиции Российской Федерации" AS column_3
FROM "rosstat-7708234640-listnormativeacts2020"
