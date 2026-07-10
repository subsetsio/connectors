SELECT
    CAST("AirPollutant" AS VARCHAR) AS "AirPollutant",
    CAST("AssessmentMethod" AS VARCHAR) AS "AssessmentMethod",
    CAST("AssessmentMethodId" AS VARCHAR) AS "AssessmentMethodId",
    CAST("AttainmentId" AS VARCHAR) AS "AttainmentId",
    CAST("B2G_Namespace" AS VARCHAR) AS "B2G_Namespace",
    CAST("Country" AS VARCHAR) AS "Country",
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("ExceedanceTypeId" AS VARCHAR) AS "ExceedanceTypeId",
    CAST("Imported" AS VARCHAR) AS "Imported",
    CAST("IsExceedance" AS VARCHAR) AS "IsExceedance",
    CAST("ObjectiveType" AS VARCHAR) AS "ObjectiveType",
    CAST("ProtectionTarget" AS VARCHAR) AS "ProtectionTarget",
    CAST("ReportingMetric" AS VARCHAR) AS "ReportingMetric",
    CAST("ReportingYear" AS VARCHAR) AS "ReportingYear",
    CAST("SourceDataURL" AS VARCHAR) AS "SourceDataURL",
    CAST("ZoneId" AS VARCHAR) AS "ZoneId"
FROM "european-environment-agency-airqualitydataflows.attainmentmethods"
