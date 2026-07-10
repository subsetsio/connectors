SELECT
    CAST("concentration2007" AS VARCHAR) AS "concentration2007",
    CAST("concentration2023" AS VARCHAR) AS "concentration2023",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("difference" AS VARCHAR) AS "difference",
    CAST("discodataUpdate" AS VARCHAR) AS "discodataUpdate",
    CAST("Indicator" AS VARCHAR) AS "Indicator",
    CAST("numberOfWaterBodies" AS VARCHAR) AS "numberOfWaterBodies",
    CAST("Percentage_change_2007_2023" AS VARCHAR) AS "Percentage_change_2007_2023",
    CAST("UoM" AS VARCHAR) AS "UoM"
FROM "european-environment-agency-bise.kcbd-nutrients-in-freshwater-in-europe"
