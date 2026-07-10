-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "disasterNumber" AS disasternumber,
    "declarationDate" AS declarationdate,
    "incidentType" AS incidenttype,
    "state",
    "county",
    "applicantName" AS applicantname,
    "educationApplicant" AS educationapplicant,
    "numberOfProjects" AS numberofprojects,
    "federalObligatedAmount" AS federalobligatedamount,
    "lastRefresh" AS lastrefresh,
    "hash"
FROM "fema-publicassistancefundedprojectssummaries"
