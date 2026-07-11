-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "end_of_day",
    "market_activities",
    "interest_payment",
    "discount_window_reversal",
    "discount_window_activities",
    "closing_balance"
FROM "hkma-market-operation-daily"
