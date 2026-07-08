SELECT
    TRY_CAST(operationDate AS DATE)      AS operation_date,
    operationId                          AS operation_id,
    TRY_CAST(settlementDate AS DATE)     AS settlement_date,
    TRY_CAST(maturityDate AS DATE)       AS maturity_date,
    cusip,
    securityDescription                  AS security_description,
    TRY_CAST(parAmtSubmitted AS DOUBLE)  AS par_amount_submitted,
    TRY_CAST(parAmtAccepted AS DOUBLE)   AS par_amount_accepted,
    TRY_CAST(weightedAverageRate AS DOUBLE) AS weighted_average_rate,
    TRY_CAST(somaHoldings AS DOUBLE)     AS soma_holdings,
    TRY_CAST(theoAvailToBorrow AS DOUBLE) AS theoretical_available,
    TRY_CAST(actualAvailToBorrow AS DOUBLE) AS actual_available,
    TRY_CAST(outstandingLoans AS DOUBLE) AS outstanding_loans
FROM "ny-fed-securities-lending"
WHERE TRY_CAST(operationDate AS DATE) IS NOT NULL AND cusip IS NOT NULL
