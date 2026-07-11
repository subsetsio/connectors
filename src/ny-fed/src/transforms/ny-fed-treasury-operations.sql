-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are security-detail lines under Treasury outright operations; operation-level context repeats across detail rows.
SELECT
    "operationId" AS operationid,
    "operationDate" AS operationdate,
    "operationType" AS operationtype,
    "operationDirection" AS operationdirection,
    "settlementDate" AS settlementdate,
    "maturityRangeStart" AS maturityrangestart,
    "maturityRangeEnd" AS maturityrangeend,
    "auctionMethod" AS auctionmethod,
    CAST("totalParAmtSubmitted" AS BIGINT) AS totalparamtsubmitted,
    CAST("totalParAmtAccepted" AS BIGINT) AS totalparamtaccepted,
    "cusip",
    "securityDescription" AS securitydescription,
    CAST("parAmountAccepted" AS BIGINT) AS paramountaccepted,
    "weightedAvgAccptPrice" AS weightedavgaccptprice,
    "leastFavoriteAccptPrice" AS leastfavoriteaccptprice
FROM "ny-fed-treasury-operations"
