-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "transactionid",
    "relatedtransactionid",
    "propertyid",
    "unitid",
    "personid",
    "contractcode",
    "operatorlastname",
    "totalamount",
    "amountpaid",
    "transactiontype",
    "transactionstatus",
    "transactionpostdate",
    "transactiondate",
    "transactiondesc",
    "chargetype"
FROM "nyc-open-data-vmkw-p55f"
