-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "disasterNumber" AS disasternumber,
    "applicantId" AS applicantid,
    "state",
    "applicantName" AS applicantname,
    "addressLine1" AS addressline1,
    "addressLine2" AS addressline2,
    "city",
    "zipCode" AS zipcode,
    "lastRefresh" AS lastrefresh,
    "hash"
FROM "fema-publicassistanceapplicants"
