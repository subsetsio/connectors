-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are collateral/security-type detail lines under repo operations; operation-level totals repeat across detail rows and should not be summed without grouping at the operation level.
SELECT
    "operationId" AS operationid,
    "operationDate" AS operationdate,
    "operationType" AS operationtype,
    "operationMethod" AS operationmethod,
    "settlementDate" AS settlementdate,
    "maturityDate" AS maturitydate,
    "term",
    "termCalenderDays" AS termcalenderdays,
    "settlementType" AS settlementtype,
    "totalAmtSubmitted" AS totalamtsubmitted,
    "totalAmtAccepted" AS totalamtaccepted,
    "securityType" AS securitytype,
    "amtSubmitted" AS amtsubmitted,
    "amtAccepted" AS amtaccepted,
    "percentOfferingRate" AS percentofferingrate,
    "percentAwardRate" AS percentawardrate,
    "percentWeightedAverageRate" AS percentweightedaveragerate
FROM "ny-fed-repo-operations"
