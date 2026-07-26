-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "invoiceid",
    "invoicesequenceid",
    "omonumber",
    "invoicestatus",
    "invoicedate",
    "invoicebillamount",
    "invoicepayamount",
    "salestax",
    "adminfee",
    "paymentid",
    "chargeamount",
    "datetransferdof",
    "unique_key"
FROM "nyc-open-data-emrz-5p35"
