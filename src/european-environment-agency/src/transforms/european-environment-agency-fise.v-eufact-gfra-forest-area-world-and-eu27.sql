SELECT
    CAST("area_percentage" AS VARCHAR) AS "area_percentage",
    CAST("country" AS VARCHAR) AS "country",
    CAST("forest_area" AS VARCHAR) AS "forest_area",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-eufact-gfra-forest-area-world-and-eu27"
