-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    CAST("Наименование должности" AS BIGINT) AS column,
    CAST("Общие требования к претенденту" AS BIGINT) AS column_2,
    CAST("Требования к образованию" AS BIGINT) AS column_3,
    CAST("Требования к профессиональному стажу" AS BIGINT) AS column_4,
    CAST("Требования к профессиональным знаниям и учениям" AS BIGINT) AS column_5,
    CAST("Режим работы" AS BIGINT) AS column_6,
    CAST("Основные условия" AS BIGINT) AS column_7,
    CAST("Размер оплаты труда" AS BIGINT) AS column_8,
    CAST("Основные государственные гарантии" AS BIGINT) AS column_9,
    CAST("Перечень необходимых документов" AS BIGINT) AS column_10,
    CAST("Дата начала приема документов" AS BIGINT) AS column_11,
    CAST("Дата окончания приема документов" AS BIGINT) AS column_12,
    CAST("Адрес приема документов" AS BIGINT) AS column_13,
    CAST("Ограничения и обязательства" AS BIGINT) AS column_14,
    CAST("ФИО контактного лица" AS BIGINT) AS column_15,
    CAST("E-mail контактного лица" AS BIGINT) AS e_mail,
    CAST("Телефон ответственного лица" AS BIGINT) AS column_16,
    CAST("Адрес подачи документов" AS BIGINT) AS column_17,
    CAST("График работы приемной комиссии" AS BIGINT) AS column_18,
    CAST("Порядок проведения конкурса" AS BIGINT) AS column_19,
    CAST("Предполагаемая дата проведения конкурса" AS BIGINT) AS column_20,
    CAST("Место проведения конкурса" AS BIGINT) AS column_21
FROM "rosstat-7708234640-murmanskregion"
