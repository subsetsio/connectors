-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acronym",
    "vendorname",
    "contractid",
    "description",
    "date",
    "amount",
    "cttyp_nm",
    "awd_meth_nm"
FROM "nyc-open-data-3ups-txji"
