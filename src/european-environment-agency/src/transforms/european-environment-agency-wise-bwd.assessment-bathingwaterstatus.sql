SELECT
    CAST("bathingWaterIdentifier" AS VARCHAR) AS "bathingWaterIdentifier",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("management" AS VARCHAR) AS "management",
    CAST("monitoringCalendar" AS VARCHAR) AS "monitoringCalendar",
    CAST("quality" AS VARCHAR) AS "quality",
    CAST("qualityOriginalClassification" AS VARCHAR) AS "qualityOriginalClassification",
    CAST("reportedSpecialisedZoneType" AS VARCHAR) AS "reportedSpecialisedZoneType",
    CAST("season" AS VARCHAR) AS "season",
    CAST("specialisedZoneType" AS VARCHAR) AS "specialisedZoneType",
    CAST("uid" AS VARCHAR) AS "uid"
FROM "european-environment-agency-wise-bwd.assessment-bathingwaterstatus"
