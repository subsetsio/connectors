-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "femaRegion" AS femaregion,
    "state",
    "stateAbbreviation" AS stateabbreviation,
    "countyName" AS countyname,
    "placeName" AS placename,
    "planType" AS plantype,
    "planId" AS planid,
    "planTitle" AS plantitle,
    "planStatus" AS planstatus,
    "apaDate" AS apadate,
    "planApprovalDate" AS planapprovaldate,
    "planExpirationDate" AS planexpirationdate,
    "jurisdictionType" AS jurisdictiontype,
    "jurisdictionStatus" AS jurisdictionstatus,
    "adoptionDate" AS adoptiondate,
    "jurisdictionApprovalDate" AS jurisdictionapprovaldate,
    "population",
    "mppGeoid" AS mppgeoid,
    "censusSource" AS censussource,
    "communityIdNumber" AS communityidnumber,
    "popCoverage" AS popcoverage
FROM "fema-hazardmitigationplanstatuses"
