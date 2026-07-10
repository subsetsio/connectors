SELECT
    CAST("AxleNumber" AS VARCHAR) AS "AxleNumber",
    CAST("CertificationNumber" AS VARCHAR) AS "CertificationNumber",
    CAST("DigestValue" AS VARCHAR) AS "DigestValue",
    CAST("SpecificRRC" AS VARCHAR) AS "SpecificRRC",
    CAST("Twintyres" AS VARCHAR) AS "Twintyres",
    CAST("TyreDimension" AS VARCHAR) AS "TyreDimension",
    CAST("Vehicle_id" AS VARCHAR) AS "Vehicle_id"
FROM "european-environment-agency-co2emission.hdv-2023-axle"
