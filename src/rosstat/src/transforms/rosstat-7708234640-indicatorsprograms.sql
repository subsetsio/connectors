-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Наименование показателя (индикатора)" AS column,
    "Единица измерения" AS column_2,
    "Значения показателей (индикаторов) подпрограммы «Официальная статистика»" AS column_3
FROM "rosstat-7708234640-indicatorsprograms"
