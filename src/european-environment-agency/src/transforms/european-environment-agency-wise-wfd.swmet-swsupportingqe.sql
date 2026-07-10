SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("hasDescriptiveData" AS VARCHAR) AS "hasDescriptiveData",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName",
    CAST("supportingQECode" AS VARCHAR) AS "supportingQECode",
    CAST("supportingQESensitivityBQE" AS VARCHAR) AS "supportingQESensitivityBQE"
FROM "european-environment-agency-wise-wfd.swmet-swsupportingqe"
