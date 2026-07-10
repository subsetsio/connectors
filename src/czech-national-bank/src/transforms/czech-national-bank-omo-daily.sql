-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The API does not provide a stable operation identifier; multiple operation rows may share the same trade date, settlement date, maturity date, operation type, and liquidity impact.
SELECT
    "operationType" AS operationtype,
    "liquidityImpact" AS liquidityimpact,
    "tradeDate" AS tradedate,
    "settlementDate" AS settlementdate,
    "maturityDate" AS maturitydate,
    "marginalRateInPercent" AS marginalrateinpercent,
    "totalBidVolumeInCZKbln" AS totalbidvolumeinczkbln,
    "totalNumberOfBids" AS totalnumberofbids,
    "minimumBidRateInPercent" AS minimumbidrateinpercent,
    "averageBidRateInPercent" AS averagebidrateinpercent,
    "maximumBidRateInPercent" AS maximumbidrateinpercent,
    "totalAllotedVolumeInCZKbln" AS totalallotedvolumeinczkbln,
    "totalNumberOfAllotedBids" AS totalnumberofallotedbids,
    "minimumAllotedRateInPercent" AS minimumallotedrateinpercent,
    "averageAllotedRateInPercent" AS averageallotedrateinpercent,
    "maximumAllotedRateInPercent" AS maximumallotedrateinpercent,
    "allotmentPercentage" AS allotmentpercentage
FROM "czech-national-bank-omo-daily"
