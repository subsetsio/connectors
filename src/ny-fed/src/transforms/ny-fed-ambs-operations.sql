SELECT
    TRY_CAST(operationDate AS DATE)      AS operation_date,
    operationId                          AS operation_id,
    operationType                        AS operation_type,
    operationDirection                   AS operation_direction,
    TRY_CAST(settlementDate AS DATE)     AS settlement_date,
    classType                            AS class_type,
    method,
    securityDescription                  AS security_description,
    inclusionExclusionFlag               AS inclusion_flag,
    TRY_CAST(totalAmtSubmittedPar AS DOUBLE) AS amount_submitted_par,
    TRY_CAST(amtAcceptedPar AS DOUBLE)       AS amount_accepted_par,
    TRY_CAST(totalAmtAcceptedPar AS DOUBLE)  AS total_amount_accepted_par
FROM "ny-fed-ambs-operations"
WHERE TRY_CAST(operationDate AS DATE) IS NOT NULL AND operationId IS NOT NULL
