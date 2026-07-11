-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are operation-detail lines under an Agency MBS operation; operation-level totals repeat across detail rows and should not be summed without grouping at the operation level.
-- caution: The source does not expose a stable non-null detail-row identifier for every row, so this table is intentionally keyless.
SELECT
    "operationId" AS operationid,
    "operationDate" AS operationdate,
    "operationType" AS operationtype,
    "operationDirection" AS operationdirection,
    "method",
    "classType" AS classtype,
    "settlementDate" AS settlementdate,
    "totalAmtSubmittedPar" AS totalamtsubmittedpar,
    "totalAmtAcceptedPar" AS totalamtacceptedpar,
    "securityDescription" AS securitydescription,
    CAST("amtAcceptedPar" AS DOUBLE) AS amtacceptedpar,
    "inclusionExclusionFlag" AS inclusionexclusionflag
FROM "ny-fed-ambs-operations"
