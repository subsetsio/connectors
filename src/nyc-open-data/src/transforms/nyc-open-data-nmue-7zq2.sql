-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permitnumber",
    "applicationtrackingid",
    "sequencenumber",
    "applicationtypeshortdesc",
    "permitstatusid",
    "permitstatusshortdesc",
    "permitseriesid",
    "permitseriesshortdesc",
    "permittypeid",
    "permittypedesc",
    "specificstipulations",
    "permitissuedate",
    "issuedworkstartdate",
    "issuedworkenddate",
    "boroughname",
    "onstreetname",
    "fromstreetname",
    "tostreetname",
    "permitteename",
    "createdon",
    "modifiedon"
FROM "nyc-open-data-nmue-7zq2"
