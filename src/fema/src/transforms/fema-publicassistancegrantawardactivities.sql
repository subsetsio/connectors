-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "disasterNumber" AS disasternumber,
    "sriaDisaster" AS sriadisaster,
    "declarationTitle" AS declarationtitle,
    "disasterType" AS disastertype,
    "incidentType" AS incidenttype,
    "declarationDate" AS declarationdate,
    "stateAbbreviation" AS stateabbreviation,
    "state",
    "county",
    "applicantId" AS applicantid,
    "applicantName" AS applicantname,
    "pnpStatus" AS pnpstatus,
    "damageCategoryCode" AS damagecategorycode,
    "federalShareObligated" AS federalshareobligated,
    "dateObligated" AS dateobligated,
    "pwNumber" AS pwnumber,
    "projectTitle" AS projecttitle,
    "versionNumber" AS versionnumber,
    "eligibilityStatus" AS eligibilitystatus,
    "fundingStatus" AS fundingstatus,
    "paCloseoutStatus" AS pacloseoutstatus,
    "id"
FROM "fema-publicassistancegrantawardactivities"
