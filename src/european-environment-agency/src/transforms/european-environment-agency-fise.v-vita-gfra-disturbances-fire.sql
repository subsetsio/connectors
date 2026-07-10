SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("of_which_on_forest" AS VARCHAR) AS "of_which_on_forest",
    CAST("total_land_area_affected_by_fire" AS VARCHAR) AS "total_land_area_affected_by_fire",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-vita-gfra-disturbances-fire"
