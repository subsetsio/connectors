-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "income_group",
    "wages_and_saleries_dollars_in_millions",
    "percentage",
    "dividends_and_interest_dollars_in_millions",
    "_percent" AS percent,
    "business_income",
    "_" AS column
FROM "nyc-open-data-gffu-ps8j"
