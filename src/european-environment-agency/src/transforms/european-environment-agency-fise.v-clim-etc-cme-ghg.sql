SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("Forest_land_remaining_forest_land" AS VARCHAR) AS "Forest_land_remaining_forest_land",
    CAST("gas" AS VARCHAR) AS "gas",
    CAST("Land_converted_to_forest_land" AS VARCHAR) AS "Land_converted_to_forest_land",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("total" AS VARCHAR) AS "total",
    CAST("Unit" AS VARCHAR) AS "Unit",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.v-clim-etc-cme-ghg"
