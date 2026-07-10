SELECT
    CAST("Agricultural_areas" AS VARCHAR) AS "Agricultural_areas",
    CAST("Artificial_surfaces" AS VARCHAR) AS "Artificial_surfaces",
    CAST("Forests_and_transitional_woodlands" AS VARCHAR) AS "Forests_and_transitional_woodlands",
    CAST("Natural_areas" AS VARCHAR) AS "Natural_areas",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("NUTS_L0" AS VARCHAR) AS "NUTS_L0",
    CAST("NUTS_LEVEL" AS VARCHAR) AS "NUTS_LEVEL",
    CAST("pct_forests_per_nuts3" AS VARCHAR) AS "pct_forests_per_nuts3",
    CAST("Total_area_km2_CLC" AS VARCHAR) AS "Total_area_km2_CLC",
    CAST("Waterbodies" AS VARCHAR) AS "Waterbodies",
    CAST("Wetlands" AS VARCHAR) AS "Wetlands"
FROM "european-environment-agency-fise.clc-nuts3-forest"
