-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("years" AS BIGINT) AS years,
    "gender_pay_gap_unadjusted",
    "value"
FROM "geostat-gender-20statistics-income-unadj-gpg-by-years"
