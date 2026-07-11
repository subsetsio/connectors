-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "adjusted_gender_pay_gap",
    CAST("years" AS BIGINT) AS years,
    "economic_activity",
    "value"
FROM "geostat-gender-20statistics-income-adj-gpg-by-year-ec-a"
