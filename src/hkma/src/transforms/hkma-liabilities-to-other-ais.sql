-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "pay_on_dem_money_call_hkd",
    "pay_on_dem_money_call_fc",
    "pay_on_dem_money_call_total",
    "repay_or_call_in_3m_hkd",
    "repay_or_call_in_3m_fc",
    "repay_or_call_in_3m_total",
    "repay_or_call_oth_than_3m_hkd",
    "repay_or_call_oth_than_3m_fc",
    "repay_or_call_oth_than_3m_total",
    "total_loans_hkd",
    "total_loans_fc",
    "total_loans"
FROM "hkma-liabilities-to-other-ais"
