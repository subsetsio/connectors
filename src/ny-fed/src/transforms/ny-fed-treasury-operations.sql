SELECT
    TRY_CAST(operationDate AS DATE)      AS operation_date,
    operationId                          AS operation_id,
    operationType                        AS operation_type,
    operationDirection                   AS operation_direction,
    TRY_CAST(settlementDate AS DATE)     AS settlement_date,
    cusip,
    securityDescription                  AS security_description,
    TRY_CAST(maturityRangeStart AS DATE) AS maturity_range_start,
    TRY_CAST(maturityRangeEnd AS DATE)   AS maturity_range_end,
    auctionMethod                        AS auction_method,
    TRY_CAST(totalParAmtSubmitted AS DOUBLE) AS par_amount_submitted,
    TRY_CAST(parAmountAccepted AS DOUBLE)    AS par_amount_accepted,
    TRY_CAST(weightedAvgAccptPrice AS DOUBLE)   AS weighted_avg_price,
    TRY_CAST(leastFavoriteAccptPrice AS DOUBLE) AS least_favorable_price
FROM "ny-fed-treasury-operations"
WHERE TRY_CAST(operationDate AS DATE) IS NOT NULL AND operationId IS NOT NULL
