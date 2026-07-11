-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Статистик үзүүлэлт" AS column,
    "Бүрэлдэхүүн" AS column_2,
    "Улирал" AS column_3,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0500-025v1"
