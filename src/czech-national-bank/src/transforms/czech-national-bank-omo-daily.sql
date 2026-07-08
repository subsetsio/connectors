SELECT DISTINCT
    CAST(tradeDate AS DATE)                    AS trade_date,
    CAST(settlementDate AS DATE)               AS settlement_date,
    CAST(maturityDate AS DATE)                 AS maturity_date,
    operationType                              AS operation_type,
    liquidityImpact                            AS liquidity_impact,
    CAST(marginalRateInPercent AS DOUBLE)      AS marginal_rate_pct,
    CAST(averageBidRateInPercent AS DOUBLE)    AS average_bid_rate_pct,
    CAST(averageAllotedRateInPercent AS DOUBLE) AS average_alloted_rate_pct,
    CAST(totalBidVolumeInCZKbln AS DOUBLE)     AS total_bid_volume_czk_bln,
    CAST(totalAllotedVolumeInCZKbln AS DOUBLE) AS total_alloted_volume_czk_bln,
    CAST(totalNumberOfBids AS INTEGER)         AS total_number_of_bids,
    CAST(totalNumberOfAllotedBids AS INTEGER)  AS total_number_of_alloted_bids,
    CAST(allotmentPercentage AS DOUBLE)        AS allotment_pct
FROM "czech-national-bank-omo-daily"
WHERE tradeDate IS NOT NULL
