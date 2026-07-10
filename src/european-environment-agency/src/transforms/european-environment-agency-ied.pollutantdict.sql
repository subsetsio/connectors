SELECT
    CAST("AirPollutantGroup" AS VARCHAR) AS "AirPollutantGroup",
    CAST("AirPriority" AS VARCHAR) AS "AirPriority",
    CAST("id" AS VARCHAR) AS "id",
    CAST("Label" AS VARCHAR) AS "Label",
    CAST("pollutant" AS VARCHAR) AS "pollutant",
    CAST("PollutantGroupId" AS VARCHAR) AS "PollutantGroupId",
    CAST("WaterPollutantGroup" AS VARCHAR) AS "WaterPollutantGroup",
    CAST("WaterPriority" AS VARCHAR) AS "WaterPriority"
FROM "european-environment-agency-ied.pollutantdict"
