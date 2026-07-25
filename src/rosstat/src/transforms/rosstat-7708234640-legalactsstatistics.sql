-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("№ п/п" AS BIGINT) AS column,
    "Наименование вида и полное наименование нормативного правового акта" AS column_2,
    "Дата утверждения акта" AS column_3,
    "Номер нормативного правового акта" AS column_4,
    "Место размещения документа" AS column_5,
    "Ссылка на текст нормативного правового акта" AS column_6
FROM "rosstat-7708234640-legalactsstatistics"
