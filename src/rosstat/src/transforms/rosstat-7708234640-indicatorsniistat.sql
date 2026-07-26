-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    "№ п/п" AS column,
    "Показатель" AS column_2,
    "единица измерения" AS column_3,
    "2013 год (факт)" AS "2013",
    "2014 год" AS "2014",
    "2015 год" AS "2015",
    "2016 год" AS "2016",
    "2017 год" AS "2017",
    "2018 год" AS "2018"
FROM "rosstat-7708234640-indicatorsniistat"
