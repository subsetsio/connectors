-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "declarationRequestNumber" AS declarationrequestnumber,
    "region",
    "stateAbbreviation" AS stateabbreviation,
    "tribalRequest" AS tribalrequest,
    "state",
    "declarationRequestDate" AS declarationrequestdate,
    "declarationRequestType" AS declarationrequesttype,
    "incidentName" AS incidentname,
    "requestedIncidentTypes" AS requestedincidenttypes,
    "currentRequestStatus" AS currentrequeststatus,
    "requestedIncidentBeginDate" AS requestedincidentbegindate,
    "requestedIncidentEndDate" AS requestedincidentenddate,
    "requestStatusDate" AS requeststatusdate,
    "ihProgramRequested" AS ihprogramrequested,
    "iaProgramRequested" AS iaprogramrequested,
    "paProgramRequested" AS paprogramrequested,
    "hmProgramRequested" AS hmprogramrequested,
    "incidentId" AS incidentid,
    "incidentBeginDate" AS incidentbegindate
FROM "fema-declarationdenials"
