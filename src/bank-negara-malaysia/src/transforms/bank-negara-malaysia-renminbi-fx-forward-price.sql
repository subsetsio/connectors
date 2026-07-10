-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row carries spot and forward points across multiple tenors; reshape by tenor before comparing forward prices.
SELECT
    "date",
    "selling_spot",
    "selling_2_weeks",
    "selling_1_month",
    "selling_2_months",
    "selling_3_months",
    "selling_4_months",
    "selling_5_months",
    "selling_6_months",
    "buying_spot",
    "buying_2_weeks",
    "buying_1_month",
    "buying_2_months",
    "buying_3_months",
    "buying_4_months",
    "buying_5_months",
    "buying_6_months"
FROM "bank-negara-malaysia-renminbi-fx-forward-price"
