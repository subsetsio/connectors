SELECT DISTINCT
    TRY_CAST(tradeDate AS DATE)          AS trade_date,
    TRY_CAST(settlementDate AS DATE)     AS settlement_date,
    TRY_CAST(maturityDate AS DATE)       AS maturity_date,
    operationType                        AS operation_type,
    counterparty,
    currency,
    TRY_CAST(termInDays AS INTEGER)      AS term_days,
    TRY_CAST(amount AS DOUBLE)           AS amount,
    TRY_CAST(interestRate AS DOUBLE)     AS interest_rate
FROM "ny-fed-fx-swaps"
WHERE TRY_CAST(tradeDate AS DATE) IS NOT NULL AND currency IS NOT NULL
