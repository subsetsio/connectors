-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permityear",
    "permitno",
    "reservationnumber",
    "valid_date",
    "busarrivaltime",
    "permitnumber",
    "companyname",
    "dayofweek",
    "numberofbuses",
    "city",
    "state",
    "zipcode",
    "issuedate",
    "permittype",
    "vehicletype",
    "buscompanyname",
    "permitqty",
    "qtyreturn",
    "return",
    "returndate",
    "conditionrestrictions",
    "placereciepthere"
FROM "nyc-open-data-vpeq-ndkd"
