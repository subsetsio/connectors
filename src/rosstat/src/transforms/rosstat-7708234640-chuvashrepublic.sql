-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Наименование должности" AS column,
    "Общие требования к претенденту" AS column_2,
    "Требования к образованию" AS column_3,
    "Требования к профессиональному стажу" AS column_4,
    "Требования к профессиональным знаниям и учениям" AS column_5,
    "Режим работы" AS column_6,
    "Основные условия" AS column_7,
    "Размер оплаты труда" AS column_8,
    "Основные государственные гарантии" AS column_9,
    "Перечень необходимых документов" AS column_10,
    "Дата начала приема документов" AS column_11,
    "Дата окончания приема документов" AS column_12,
    "Адрес приема документов" AS column_13,
    "Ограничения и обязательства" AS column_14,
    "ФИО контактного лица" AS column_15,
    "E-mail контактного лица" AS e_mail,
    "Телефон ответственного лица" AS column_16,
    "Адрес подачи документов" AS column_17,
    "График работы приемной комиссии" AS column_18,
    "Порядок проведения конкурса" AS column_19,
    "Предполагаемая дата проведения конкурса" AS column_20,
    "Место проведения конкурса" AS column_21
FROM "rosstat-7708234640-chuvashrepublic"
