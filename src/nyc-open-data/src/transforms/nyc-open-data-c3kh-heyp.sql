-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "companyid",
    "companyname",
    "validdates",
    "permitno",
    "expirationdate",
    "issuedate",
    "permitprintdate",
    "validtimes",
    "effectivedate",
    "permitpurpose",
    "permitqty",
    "qtyreturn",
    "conditionrestrictions",
    "return",
    "returndate"
FROM "nyc-open-data-c3kh-heyp"
