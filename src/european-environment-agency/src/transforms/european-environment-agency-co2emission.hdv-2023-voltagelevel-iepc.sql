SELECT
    CAST("IEPCId" AS VARCHAR) AS "IEPCId",
    CAST("MaxContinuousPower" AS VARCHAR) AS "MaxContinuousPower",
    CAST("vehicle_id" AS VARCHAR) AS "vehicle_id",
    CAST("Voltage" AS VARCHAR) AS "Voltage"
FROM "european-environment-agency-co2emission.hdv-2023-voltagelevel-iepc"
