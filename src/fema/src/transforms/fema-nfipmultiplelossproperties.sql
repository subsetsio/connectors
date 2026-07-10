-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fipsCountyCode" AS fipscountycode,
    "state",
    "stateAbbreviation" AS stateabbreviation,
    "county",
    "zipCode" AS zipcode,
    "reportedCity" AS reportedcity,
    "communityIdNumber" AS communityidnumber,
    "communityName" AS communityname,
    "censusBlockGroup" AS censusblockgroup,
    "nfipRl" AS nfiprl,
    "nfipSrl" AS nfipsrl,
    "fmaRl" AS fmarl,
    "fmaSrl" AS fmasrl,
    "asOfDate" AS asofdate,
    "floodZone" AS floodzone,
    "latitude",
    "longitude",
    "occupancyType" AS occupancytype,
    "originalConstructionDate" AS originalconstructiondate,
    "originalNBDate" AS originalnbdate,
    "postFIRMConstructionIndicator" AS postfirmconstructionindicator,
    "primaryResidenceIndicator" AS primaryresidenceindicator,
    "mitigatedIndicator" AS mitigatedindicator,
    "insuredIndicator" AS insuredindicator,
    "totalLosses" AS totallosses,
    "mostRecentDateofLoss" AS mostrecentdateofloss,
    "id"
FROM "fema-nfipmultiplelossproperties"
