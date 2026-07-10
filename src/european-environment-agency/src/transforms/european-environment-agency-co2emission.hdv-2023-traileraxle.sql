SELECT
    CAST("AxleNumber" AS VARCHAR) AS "AxleNumber",
    CAST("Liftable" AS VARCHAR) AS "Liftable",
    CAST("Steered" AS VARCHAR) AS "Steered",
    CAST("TwinTyres" AS VARCHAR) AS "TwinTyres",
    CAST("Tyre_CertificationNumber" AS VARCHAR) AS "Tyre_CertificationNumber",
    CAST("Tyre_Dimension" AS VARCHAR) AS "Tyre_Dimension",
    CAST("Tyre_FuelEfficiencyClass" AS VARCHAR) AS "Tyre_FuelEfficiencyClass",
    CAST("Tyre_Hash" AS VARCHAR) AS "Tyre_Hash",
    CAST("Tyre_RRCDeclared" AS VARCHAR) AS "Tyre_RRCDeclared",
    CAST("vehicle_id" AS VARCHAR) AS "vehicle_id"
FROM "european-environment-agency-co2emission.hdv-2023-traileraxle"
