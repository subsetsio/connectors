SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("forest" AS VARCHAR) AS "forest",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("other_wooded_land" AS VARCHAR) AS "other_wooded_land",
    CAST("total_forest_and_other_wooded_land" AS VARCHAR) AS "total_forest_and_other_wooded_land",
    CAST("units" AS VARCHAR) AS "units",
    CAST("variable" AS VARCHAR) AS "variable",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-vita-foresteurope-forest-area-with-damage"
