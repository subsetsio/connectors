-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "disasterNumber" AS disasternumber,
    "state",
    "femaDeclarationString" AS femadeclarationstring,
    "declarationType" AS declarationtype,
    "declarationDate" AS declarationdate,
    "fyDeclared" AS fydeclared,
    "incidentType" AS incidenttype,
    "declarationTitle" AS declarationtitle,
    "ihProgramDeclared" AS ihprogramdeclared,
    "iaProgramDeclared" AS iaprogramdeclared,
    "paProgramDeclared" AS paprogramdeclared,
    "hmProgramDeclared" AS hmprogramdeclared,
    "incidentBeginDate" AS incidentbegindate,
    "incidentEndDate" AS incidentenddate,
    "disasterCloseoutDate" AS disastercloseoutdate,
    "tribalRequest" AS tribalrequest,
    "fipsStateCode" AS fipsstatecode,
    "fipsCountyCode" AS fipscountycode,
    CAST("placeCode" AS BIGINT) AS placecode,
    "designatedArea" AS designatedarea,
    CAST("declarationRequestNumber" AS BIGINT) AS declarationrequestnumber,
    "lastIAFilingDate" AS lastiafilingdate,
    CAST("incidentId" AS BIGINT) AS incidentid,
    "region",
    "designatedIncidentTypes" AS designatedincidenttypes,
    "lastRefresh" AS lastrefresh,
    "hash"
FROM "fema-disasterdeclarationssummaries"
