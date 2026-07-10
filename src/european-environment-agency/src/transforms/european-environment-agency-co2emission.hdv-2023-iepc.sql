SELECT
    CAST("CertificationMethod" AS VARCHAR) AS "CertificationMethod",
    CAST("CertificationNumber" AS VARCHAR) AS "CertificationNumber",
    CAST("DesignTypeWheelMotor" AS VARCHAR) AS "DesignTypeWheelMotor",
    CAST("DifferentialIncluded" AS VARCHAR) AS "DifferentialIncluded",
    CAST("DigestValue" AS VARCHAR) AS "DigestValue",
    CAST("LowestTotalTransmissionRatio" AS VARCHAR) AS "LowestTotalTransmissionRatio",
    CAST("NrOfGears" AS VARCHAR) AS "NrOfGears",
    CAST("RatedPower" AS VARCHAR) AS "RatedPower",
    CAST("vehicle_id" AS VARCHAR) AS "vehicle_id"
FROM "european-environment-agency-co2emission.hdv-2023-iepc"
