SELECT
    CAST("CertificationMethod" AS VARCHAR) AS "CertificationMethod",
    CAST("CertificationNumber" AS VARCHAR) AS "CertificationNumber",
    CAST("CountAtPosition" AS VARCHAR) AS "CountAtPosition",
    CAST("DigestValue" AS VARCHAR) AS "DigestValue",
    CAST("ElectricMachine_id" AS VARCHAR) AS "ElectricMachine_id",
    CAST("ElectricMachineType" AS VARCHAR) AS "ElectricMachineType",
    CAST("Position" AS VARCHAR) AS "Position",
    CAST("RatedPower" AS VARCHAR) AS "RatedPower",
    CAST("Vehicle_id" AS VARCHAR) AS "Vehicle_id"
FROM "european-environment-agency-co2emission.hdv-2023-electricmachine"
