-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The upstream period-average endpoint contains a duplicate reporting period in the raw feed, so the pass-through table is intentionally keyless.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "specific_data",
    "market_activities_injection",
    "market_activities_withdrawal",
    "interest_payment",
    "discount_window_reversal_injection",
    "discount_window_reversal_withdrawal",
    "discount_window_activities_lending",
    "discount_window_activities_borrowing",
    "closing_balance"
FROM "hkma-market-operation-periodaverage"
