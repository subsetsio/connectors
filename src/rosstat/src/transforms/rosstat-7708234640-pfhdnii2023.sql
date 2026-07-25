-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    "№ п/п" AS column,
    "Наименование показателя" AS column_2,
    "Код строки" AS column_3,
    "Код по бюджетной классификации Российской Федерации (3)" AS 3,
    "Сумма" AS column_4
FROM "rosstat-7708234640-pfhdnii2023"
