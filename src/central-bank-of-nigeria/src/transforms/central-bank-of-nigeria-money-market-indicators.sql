-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Every column is a percent-per-annum rate but they are not one series: policy rates (`mpr`, `mrr`), market rates (`interBankCallRate`, `treasuryBill`) and bank deposit/lending rates coexist in a row and must not be averaged together.
-- caution: `mrr` (the old minimum rediscount rate) was retired in favour of `mpr` and is present for only ~4% of rows; an `mpr` of `0.00` in the early rows means not-yet-adopted rather than a zero policy rate.
SELECT
    "id",
    "tyear",
    "tmonth",
    "period",
    "interBankCallRate" AS interbankcallrate,
    "mrr",
    CAST("mpr" AS DOUBLE) AS mpr,
    CAST("treasuryBill" AS DOUBLE) AS treasurybill,
    CAST("savingsDeposit" AS DOUBLE) AS savingsdeposit,
    CAST("oneMonthDeposit" AS DOUBLE) AS onemonthdeposit,
    CAST("threeMonthsDeposit" AS DOUBLE) AS threemonthsdeposit,
    CAST("sixMonthsDeposit" AS DOUBLE) AS sixmonthsdeposit,
    CAST("twelveMonthsDeposit" AS DOUBLE) AS twelvemonthsdeposit,
    CAST("primeLending" AS DOUBLE) AS primelending,
    CAST("maxLending" AS DOUBLE) AS maxlending
FROM "central-bank-of-nigeria-money-market-indicators"
