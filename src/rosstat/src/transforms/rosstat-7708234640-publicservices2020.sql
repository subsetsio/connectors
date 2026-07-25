-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    "Отчетный период" AS column,
    "Количество зарегистрированных заявлений 
от заявителей на предоставление услуги" AS column_2,
    "Количество заявлений, 
на которые за отчетный период был направлен ответ заявителю 
в установленный срок" AS column_3,
    "Количество поступивших жалоб заявителей 
на качество предоставления услуг" AS column_4
FROM "rosstat-7708234640-publicservices2020"
