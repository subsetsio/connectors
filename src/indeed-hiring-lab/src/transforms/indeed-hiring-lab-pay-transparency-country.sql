-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "country_code",
    "country",
    CAST("pay_transparency_pct" AS DOUBLE) AS pay_transparency_pct,
    "pay_transparency_pct_3ma"
FROM "indeed-hiring-lab-pay-transparency-country"
