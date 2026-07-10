SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("numberOfBathingWaters" AS VARCHAR) AS "numberOfBathingWaters",
    CAST("quality" AS VARCHAR) AS "quality",
    CAST("season" AS VARCHAR) AS "season",
    CAST("specialisedZoneType" AS VARCHAR) AS "specialisedZoneType"
FROM "european-environment-agency-wise-bwd.assessment-bathingwaterstatus-country"
