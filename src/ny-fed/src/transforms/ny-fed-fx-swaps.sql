-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tradeDate" AS tradedate,
    "settlementDate" AS settlementdate,
    "maturityDate" AS maturitydate,
    "operationType" AS operationtype,
    "counterparty",
    "currency",
    "termInDays" AS termindays,
    "amount",
    "interestRate" AS interestrate,
    "isSmallValue" AS issmallvalue,
    "lastUpdated" AS lastupdated
FROM "ny-fed-fx-swaps"
