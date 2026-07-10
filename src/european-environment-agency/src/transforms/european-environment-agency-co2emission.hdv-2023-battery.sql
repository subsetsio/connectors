SELECT
    CAST("Capacitance" AS VARCHAR) AS "Capacitance",
    CAST("CertificationMethod" AS VARCHAR) AS "CertificationMethod",
    CAST("CertificationNumber" AS VARCHAR) AS "CertificationNumber",
    CAST("DigestValue" AS VARCHAR) AS "DigestValue",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("MaxVoltage" AS VARCHAR) AS "MaxVoltage",
    CAST("MinVoltage" AS VARCHAR) AS "MinVoltage",
    CAST("NominalVoltage" AS VARCHAR) AS "NominalVoltage",
    CAST("TotalStorageCapacity" AS VARCHAR) AS "TotalStorageCapacity",
    CAST("TotalStorageCapacity_unit" AS VARCHAR) AS "TotalStorageCapacity_unit",
    CAST("TotalUsableCapacityInSimulation" AS VARCHAR) AS "TotalUsableCapacityInSimulation",
    CAST("TotalUsableCapacityInSimulation_unit" AS VARCHAR) AS "TotalUsableCapacityInSimulation_unit",
    CAST("Vehicle_id" AS VARCHAR) AS "Vehicle_id"
FROM "european-environment-agency-co2emission.hdv-2023-battery"
