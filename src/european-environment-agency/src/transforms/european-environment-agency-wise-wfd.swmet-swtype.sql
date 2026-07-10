SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("hasDescriptiveData" AS VARCHAR) AS "hasDescriptiveData",
    CAST("NCSWaterBodyType" AS VARCHAR) AS "NCSWaterBodyType",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName",
    CAST("swTypeCategory" AS VARCHAR) AS "swTypeCategory",
    CAST("swTypeCode" AS VARCHAR) AS "swTypeCode",
    CAST("swTypeDescription" AS VARCHAR) AS "swTypeDescription",
    CAST("swTypeSpecificHyMoConditions" AS VARCHAR) AS "swTypeSpecificHyMoConditions",
    CAST("swTypeSpecificPhysChemConditions" AS VARCHAR) AS "swTypeSpecificPhysChemConditions",
    CAST("swTypeSpecificReferenceConditionsForBQEs" AS VARCHAR) AS "swTypeSpecificReferenceConditionsForBQEs"
FROM "european-environment-agency-wise-wfd.swmet-swtype"
