-- the two bid-rate ranges stay VARCHAR: 21% / 24% of values do not split into two clean numbers
SELECT
    CAST("id" AS BIGINT) AS source_row_id,
    CAST("auctionDate_iso" AS DATE) AS auction_date,
    NULLIF(TRIM("securityType"), '') AS security_type,
    NULLIF(TRIM("tenor"), '') AS tenor,
    NULLIF(TRIM("auctionNo"), '') AS auction_no,
    NULLIF(TRIM("auction"), '') AS auction_window,
    NULLIF(TRIM("week"), '') AS week_of_month,
    CAST("maturityDate_iso" AS DATE) AS maturity_date,
    TRY_CAST(NULLIF(TRIM("totalSubscription"), '') AS DOUBLE) AS total_subscription,
    TRY_CAST(NULLIF(TRIM("totalSuccessful"), '') AS DOUBLE) AS total_successful,
    NULLIF(TRIM("rangeBid"), '') AS bid_rate_range,
    NULLIF(TRIM("successfulBidRates"), '') AS successful_bid_rate_range,
    NULLIF(TRIM("rateDescription"), '') AS rate_description,
    TRY_CAST(NULLIF(TRIM("rate"), '') AS DOUBLE) AS rate,
    TRY_CAST(NULLIF(TRIM("trueYield"), '') AS DOUBLE) AS true_yield,
    TRY_CAST(NULLIF(TRIM("amtOffered"), '') AS DOUBLE) AS amount_offered,
    TRY_CAST(NULLIF(TRIM("totalAmtRepaid"), '') AS DOUBLE) AS total_amount_repaid,
    NULLIF(TRIM("netType"), '') AS net_type,
    TRY_CAST(NULLIF(TRIM("netValue"), '') AS DOUBLE) AS net_value
FROM "central-bank-of-nigeria-securities-auctions"
