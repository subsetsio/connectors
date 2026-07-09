-- `id` and the `period` label are dropped: (year, month) is the source's real grain
SELECT
    CAST("period_start_iso" AS DATE) AS month_start,
    CAST("tyear" AS BIGINT) AS year,
    CAST("tmonth" AS BIGINT) AS month,
    TRY_CAST(NULLIF(TRIM("interBankCallRate"), '') AS DOUBLE) AS interbank_call_rate,
    TRY_CAST(NULLIF(TRIM("mrr"), '') AS DOUBLE) AS mrr,
    TRY_CAST(NULLIF(TRIM("mpr"), '') AS DOUBLE) AS mpr,
    TRY_CAST(NULLIF(TRIM("treasuryBill"), '') AS DOUBLE) AS treasury_bill_rate,
    TRY_CAST(NULLIF(TRIM("savingsDeposit"), '') AS DOUBLE) AS savings_deposit_rate,
    TRY_CAST(NULLIF(TRIM("oneMonthDeposit"), '') AS DOUBLE) AS one_month_deposit_rate,
    TRY_CAST(NULLIF(TRIM("threeMonthsDeposit"), '') AS DOUBLE) AS three_month_deposit_rate,
    TRY_CAST(NULLIF(TRIM("sixMonthsDeposit"), '') AS DOUBLE) AS six_month_deposit_rate,
    TRY_CAST(NULLIF(TRIM("twelveMonthsDeposit"), '') AS DOUBLE) AS twelve_month_deposit_rate,
    TRY_CAST(NULLIF(TRIM("primeLending"), '') AS DOUBLE) AS prime_lending_rate,
    TRY_CAST(NULLIF(TRIM("maxLending"), '') AS DOUBLE) AS max_lending_rate
FROM "central-bank-of-nigeria-money-market-indicators"
