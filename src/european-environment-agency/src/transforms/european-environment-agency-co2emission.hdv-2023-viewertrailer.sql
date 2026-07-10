SELECT
    CAST("CO2v" AS VARCHAR) AS "CO2v",
    CAST("MS_BodyWorkCode" AS VARCHAR) AS "MS_BodyWorkCode",
    CAST("MS_RegistrationCountry" AS VARCHAR) AS "MS_RegistrationCountry",
    CAST("MS_RegistrationDateClean_YYYYMMDD" AS VARCHAR) AS "MS_RegistrationDateClean_YYYYMMDD",
    CAST("MS_StageOfCompletionCode" AS VARCHAR) AS "MS_StageOfCompletionCode",
    CAST("MS_TPMLM" AS VARCHAR) AS "MS_TPMLM",
    CAST("MS_VehicleCategoryCode" AS VARCHAR) AS "MS_VehicleCategoryCode",
    CAST("MS_Vocational" AS VARCHAR) AS "MS_Vocational",
    CAST("OEM_Make" AS VARCHAR) AS "OEM_Make",
    CAST("OEM_ManufacturerName" AS VARCHAR) AS "OEM_ManufacturerName",
    CAST("OEM_ModelCommercialName" AS VARCHAR) AS "OEM_ModelCommercialName",
    CAST("OEM_TPMLM" AS VARCHAR) AS "OEM_TPMLM",
    CAST("OEM_VehicleGroup" AS VARCHAR) AS "OEM_VehicleGroup",
    CAST("OEM_VehicleSubGroup" AS VARCHAR) AS "OEM_VehicleSubGroup",
    CAST("vehicle_id" AS VARCHAR) AS "vehicle_id"
FROM "european-environment-agency-co2emission.hdv-2023-viewertrailer"
