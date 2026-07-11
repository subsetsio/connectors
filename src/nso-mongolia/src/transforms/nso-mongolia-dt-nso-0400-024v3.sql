-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Хүйс" AS column,
    "Хариуцлагын хэлбэр" AS column_2,
    strptime("Сар", '%Y-%m')::DATE AS column_3,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0400-024v3"
