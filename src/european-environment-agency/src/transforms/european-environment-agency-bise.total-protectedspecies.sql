SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("Lastest_Discodata_update" AS VARCHAR) AS "Lastest_Discodata_update",
    CAST("Species_Art12" AS VARCHAR) AS "Species_Art12",
    CAST("Species_Art17" AS VARCHAR) AS "Species_Art17",
    CAST("Total_Species_Art17_12" AS VARCHAR) AS "Total_Species_Art17_12"
FROM "european-environment-agency-bise.total-protectedspecies"
