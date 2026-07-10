-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row carries multiple tenor columns for the same product and date; unpivot tenors before comparing or aggregating rates across maturities.
SELECT
    "date",
    "overnight",
    "week_1",
    "month_1",
    "month_3",
    "month_6",
    "year_1",
    "product"
FROM "bank-negara-malaysia-interest-rate"
