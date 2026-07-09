-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: JISDOR is a USD/IDR reference fixing, not a buy/sell quote; compare it to transaction-rate midpoints only with that methodological difference in mind.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "currency",
    "unit",
    "buy",
    "sell"
FROM "bank-indonesia-jisdor"
