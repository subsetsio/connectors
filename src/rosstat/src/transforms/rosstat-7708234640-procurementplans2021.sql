-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    "№ п/п" AS column,
    "Идентификационный код закупки" AS column_2,
    "Объект закупки      Код товара, работы, услуги по Общероссийскому классификатору продукции по видам экономической деятельности ОК 034-2014 (КПЕС 2008) (ОКПД2)" AS 034_2014_2008_2,
    "Наименование услуги, товара, работы" AS column_3,
    "Наименование объекта закупки" AS column_4,
    "Планируемый год размещения извещения об осуществлении закупки, направления приглашения принять участие в определении поставщика (подрядчика, исполнителя), заключения контракта с единственным поставщиком (подрядчиком, исполнителем)" AS column_5,
    "Объем финансового обеспечения, в том числе планируемые платежи" AS column_6,
    "Информация о проведении обязательного общественного обсуждения закупки" AS column_7,
    "Наименование уполномоченного органа (учреждения)" AS column_8,
    "Наименование организатора проведения совместного конкурса или аукциона" AS column_9
FROM "rosstat-7708234640-procurementplans2021"
