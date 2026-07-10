SELECT
    CAST("addressConfidentiality" AS VARCHAR) AS "addressConfidentiality",
    CAST("buildingNumber" AS VARCHAR) AS "buildingNumber",
    CAST("city" AS VARCHAR) AS "city",
    CAST("controlFileId" AS VARCHAR) AS "controlFileId",
    CAST("electronicMailAddress" AS VARCHAR) AS "electronicMailAddress",
    CAST("faxNo" AS VARCHAR) AS "faxNo",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("individualName" AS VARCHAR) AS "individualName",
    CAST("installationId" AS VARCHAR) AS "installationId",
    CAST("organisationName" AS VARCHAR) AS "organisationName",
    CAST("postalCode" AS VARCHAR) AS "postalCode",
    CAST("streetName" AS VARCHAR) AS "streetName",
    CAST("telephoneNo" AS VARCHAR) AS "telephoneNo"
FROM "european-environment-agency-ied.productioninstallationcapermit"
