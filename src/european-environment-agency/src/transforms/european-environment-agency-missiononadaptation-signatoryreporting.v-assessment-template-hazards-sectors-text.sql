SELECT
    CAST("Category" AS VARCHAR) AS "Category",
    CAST("Category_Id" AS VARCHAR) AS "Category_Id",
    CAST("Hazard" AS VARCHAR) AS "Hazard",
    CAST("Hazard_Id" AS VARCHAR) AS "Hazard_Id",
    CAST("Id" AS VARCHAR) AS "Id",
    CAST("Language" AS VARCHAR) AS "Language",
    CAST("Order" AS VARCHAR) AS "Order",
    CAST("Sector" AS VARCHAR) AS "Sector",
    CAST("Signatory" AS VARCHAR) AS "Signatory"
FROM "european-environment-agency-missiononadaptation-signatoryreporting.v-assessment-template-hazards-sectors-text"
