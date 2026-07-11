-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source does not expose a stable non-null detail-row identifier for every row, so this table is intentionally keyless.
SELECT
    "operationId" AS operationid,
    "operationDate" AS operationdate,
    "operationType" AS operationtype,
    "settlementDate" AS settlementdate,
    "maturityDate" AS maturitydate,
    "cusip",
    "securityDescription" AS securitydescription,
    "parAmtSubmitted" AS paramtsubmitted,
    "parAmtAccepted" AS paramtaccepted,
    "weightedAverageRate" AS weightedaveragerate,
    "somaHoldings" AS somaholdings,
    "theoAvailToBorrow" AS theoavailtoborrow,
    "actualAvailToBorrow" AS actualavailtoborrow,
    "outstandingLoans" AS outstandingloans
FROM "ny-fed-securities-lending"
