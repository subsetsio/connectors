-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "projectIdentifier" AS projectidentifier,
    "transactionIdentifier" AS transactionidentifier,
    "transactionDate" AS transactiondate,
    "commitmentIdentifier" AS commitmentidentifier,
    "accsLine" AS accsline,
    "fundCode" AS fundcode,
    "federalShareProjectCostAmt" AS federalshareprojectcostamt,
    "recipientAdminCostAmt" AS recipientadmincostamt,
    "subrecipientAdminCostAmt" AS subrecipientadmincostamt,
    "subrecipientMgmtCostAmt" AS subrecipientmgmtcostamt,
    "id"
FROM "fema-hazardmitigationassistanceprojectsfinancialtransactions"
