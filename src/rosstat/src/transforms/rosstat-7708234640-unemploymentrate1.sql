-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "№ п/п" AS column,
    "Федеральные округа и субъекты Российской Федерации" AS column_2,
    "Уровень безработицы (по данным выборочных обследований рабочей силы; в процентах)" AS column_3
FROM "rosstat-7708234640-unemploymentrate1"
