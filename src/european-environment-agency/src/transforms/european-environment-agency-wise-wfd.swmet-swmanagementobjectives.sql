SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("hasDescriptiveData" AS VARCHAR) AS "hasDescriptiveData",
    CAST("managementObjectivesContinuity" AS VARCHAR) AS "managementObjectivesContinuity",
    CAST("managementObjectivesContinuityQuantitative" AS VARCHAR) AS "managementObjectivesContinuityQuantitative",
    CAST("managementObjectivesNutrients" AS VARCHAR) AS "managementObjectivesNutrients",
    CAST("managementObjectivesNutrientsQuantitativeN" AS VARCHAR) AS "managementObjectivesNutrientsQuantitativeN",
    CAST("managementObjectivesNutrientsQuantitativeP" AS VARCHAR) AS "managementObjectivesNutrientsQuantitativeP",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName",
    CAST("waterResourcePlans" AS VARCHAR) AS "waterResourcePlans"
FROM "european-environment-agency-wise-wfd.swmet-swmanagementobjectives"
