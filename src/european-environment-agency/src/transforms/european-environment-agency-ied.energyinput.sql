SELECT
    CAST("confidentialityReason" AS VARCHAR) AS "confidentialityReason",
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("energyinputTJ" AS VARCHAR) AS "energyinputTJ",
    CAST("fuelInput" AS VARCHAR) AS "fuelInput",
    CAST("furtherDetails" AS VARCHAR) AS "furtherDetails",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("installationPartReportId" AS VARCHAR) AS "installationPartReportId",
    CAST("otherGaseousFuel" AS VARCHAR) AS "otherGaseousFuel",
    CAST("otherSolidFuel" AS VARCHAR) AS "otherSolidFuel"
FROM "european-environment-agency-ied.energyinput"
