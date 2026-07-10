-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "disasterNumber" AS disasternumber,
    "declarationDate" AS declarationdate,
    "disasterName" AS disastername,
    "incidentBeginDate" AS incidentbegindate,
    "incidentEndDate" AS incidentenddate,
    "declarationType" AS declarationtype,
    "stateCode" AS statecode,
    "stateName" AS statename,
    "incidentType" AS incidenttype,
    "entryDate" AS entrydate,
    "updateDate" AS updatedate,
    "closeoutDate" AS closeoutdate,
    "region",
    "ihProgramDeclared" AS ihprogramdeclared,
    "iaProgramDeclared" AS iaprogramdeclared,
    "paProgramDeclared" AS paprogramdeclared,
    "hmProgramDeclared" AS hmprogramdeclared,
    "designatedIncidentTypes" AS designatedincidenttypes,
    "declarationRequestDate" AS declarationrequestdate,
    "disasterPageUrl" AS disasterpageurl,
    "shapefileUrl" AS shapefileurl,
    "kmzfileUrl" AS kmzfileurl,
    "geoJsonUrl" AS geojsonurl,
    "lastRefresh" AS lastrefresh,
    "hash"
FROM "fema-femawebdisasterdeclarations"
