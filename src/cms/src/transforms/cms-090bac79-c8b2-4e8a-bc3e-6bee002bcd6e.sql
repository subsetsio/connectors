-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Characteristics" AS characteristics,
    CAST("Home_ownership" AS DOUBLE) AS home_ownership,
    CAST("Own_bank_deposit_accounts" AS DOUBLE) AS own_bank_deposit_accounts,
    CAST("Checking_account" AS DOUBLE) AS checking_account,
    CAST("Savings_account" AS DOUBLE) AS savings_account,
    "Certificates_of_deposit" AS certificates_of_deposit,
    "Stocks_or_mutual_funds" AS stocks_or_mutual_funds,
    "Retirement_accounts" AS retirement_accounts,
    CAST("Receive_social_security" AS DOUBLE) AS receive_social_security,
    "Receive_supplemental_security_income" AS receive_supplemental_security_income,
    "Receive_pension" AS receive_pension,
    "Got_paid_to_work_last_month" AS got_paid_to_work_last_month,
    CAST("Median_combined_income" AS BIGINT) AS median_combined_income,
    "Median_combined_earnings" AS median_combined_earnings,
    "Median_monthly_earnings" AS median_monthly_earnings,
    "Median_home_equity" AS median_home_equity,
    "Median_comb_val_of_bank_deposit_acc" AS median_comb_val_of_bank_deposit_acc,
    "Median_combined_stocks_mutual_funds" AS median_combined_stocks_mutual_funds,
    "Median_combined_retirement_accounts" AS median_combined_retirement_accounts,
    "Median_combined_amount_received_retirement_accounts" AS median_combined_amount_received_retirement_accounts,
    CAST("Median_combined_social_security_payments" AS BIGINT) AS median_combined_social_security_payments,
    "Median_combined_pension_payments" AS median_combined_pension_payments
FROM "cms-090bac79-c8b2-4e8a-bc3e-6bee002bcd6e"
