SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("hasDescriptiveData" AS VARCHAR) AS "hasDescriptiveData",
    CAST("keyTypeMeasure" AS VARCHAR) AS "keyTypeMeasure",
    CAST("keyTypeMeasureOther" AS VARCHAR) AS "keyTypeMeasureOther",
    CAST("measureCode" AS VARCHAR) AS "measureCode",
    CAST("measureName" AS VARCHAR) AS "measureName",
    CAST("measureType" AS VARCHAR) AS "measureType",
    CAST("msfdRelevance" AS VARCHAR) AS "msfdRelevance",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName"
FROM "european-environment-agency-wise-wfd.rbmppom-ktm-measure"
