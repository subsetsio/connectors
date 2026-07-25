-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "№ п/п" AS column,
    "Наименование показателя (индикатора)" AS column_2,
    "Единица измерения" AS column_3,
    "Значения показателей (индикаторов) государственной программы, подпрограммы государственной программы, федеральной целевой программы (подпрограммы федеральной целевой программы)" AS column_4,
    "Расчет значений показателей (индикаторов) в соответствии с утвержденной методикой расчета показателей (индикаторов)" AS column_5,
    "Обоснование отклонений значений показателя (индикатора) на конец отчетного года (при наличии)" AS column_6
FROM "rosstat-7708234640-indicatorsprograms2020"
