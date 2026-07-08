SELECT
    TRY_CAST(operationDate AS DATE)      AS operation_date,
    operationId                          AS operation_id,
    operationType                        AS operation_type,
    operationMethod                      AS operation_method,
    TRY_CAST(settlementDate AS DATE)     AS settlement_date,
    TRY_CAST(maturityDate AS DATE)       AS maturity_date,
    term,
    TRY_CAST(termCalenderDays AS INTEGER) AS term_calendar_days,
    settlementType                       AS settlement_type,
    securityType                         AS security_type,
    TRY_CAST(amtSubmitted AS DOUBLE)     AS amount_submitted,
    TRY_CAST(amtAccepted AS DOUBLE)      AS amount_accepted,
    TRY_CAST(totalAmtSubmitted AS DOUBLE) AS total_amount_submitted,
    TRY_CAST(totalAmtAccepted AS DOUBLE)  AS total_amount_accepted,
    TRY_CAST(percentOfferingRate AS DOUBLE)        AS offering_rate,
    TRY_CAST(percentAwardRate AS DOUBLE)           AS award_rate,
    TRY_CAST(percentWeightedAverageRate AS DOUBLE) AS weighted_average_rate
FROM "ny-fed-repo-operations"
WHERE TRY_CAST(operationDate AS DATE) IS NOT NULL AND operationId IS NOT NULL
