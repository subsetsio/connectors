SELECT
    CAST("Category_Name" AS VARCHAR) AS "Category_Name",
    CAST("Category_Order" AS VARCHAR) AS "Category_Order",
    CAST("CategoryId" AS VARCHAR) AS "CategoryId",
    CAST("Sector_Name" AS VARCHAR) AS "Sector_Name",
    CAST("Sector_Order" AS VARCHAR) AS "Sector_Order",
    CAST("SectorId" AS VARCHAR) AS "SectorId"
FROM "european-environment-agency-missiononadaptation.v-planning-template-adaptation-goals-grouped-sectors-text"
