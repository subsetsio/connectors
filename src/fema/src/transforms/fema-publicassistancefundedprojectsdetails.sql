-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "disasterNumber" AS disasternumber,
    "declarationDate" AS declarationdate,
    "incidentType" AS incidenttype,
    "pwNumber" AS pwnumber,
    "applicationTitle" AS applicationtitle,
    "applicantId" AS applicantid,
    "damageCategoryCode" AS damagecategorycode,
    "damageCategoryDescrip" AS damagecategorydescrip,
    "projectStatus" AS projectstatus,
    "projectProcessStep" AS projectprocessstep,
    "projectSize" AS projectsize,
    "county",
    CAST("countyCode" AS BIGINT) AS countycode,
    "stateAbbreviation" AS stateabbreviation,
    CAST("stateNumberCode" AS BIGINT) AS statenumbercode,
    "projectAmount" AS projectamount,
    "federalShareObligated" AS federalshareobligated,
    "totalObligated" AS totalobligated,
    "lastObligationDate" AS lastobligationdate,
    "firstObligationDate" AS firstobligationdate,
    "mitigationAmount" AS mitigationamount,
    "gmProjectId" AS gmprojectid,
    "gmApplicantId" AS gmapplicantid,
    "lastRefresh" AS lastrefresh,
    "hash"
FROM "fema-publicassistancefundedprojectsdetails"
