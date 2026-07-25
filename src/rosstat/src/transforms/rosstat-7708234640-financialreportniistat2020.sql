-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "№ п/п" AS column,
    "Наименование показателя" AS column_2,
    "Утверждено плановых назначений, руб." AS column_3,
    "Исполнено плановых назначений, руб." AS column_4
FROM "rosstat-7708234640-financialreportniistat2020"
