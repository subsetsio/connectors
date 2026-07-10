-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "subapplicationIdentifier" AS subapplicationidentifier,
    "transactionType" AS transactiontype,
    "transactionDate" AS transactiondate,
    "commitmentIdentifier" AS commitmentidentifier,
    "paymentNumber" AS paymentnumber,
    "accsLine" AS accsline,
    "fundCode" AS fundcode,
    "amount",
    "id"
FROM "fema-hmasubapplicationsfinancialtransactions"
