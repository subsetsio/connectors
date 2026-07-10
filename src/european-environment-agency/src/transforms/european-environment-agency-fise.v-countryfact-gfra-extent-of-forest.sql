SELECT
    CAST("forest_area" AS VARCHAR) AS "forest_area",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("other_land" AS VARCHAR) AS "other_land",
    CAST("other_wooded_land" AS VARCHAR) AS "other_wooded_land",
    CAST("total_land_area" AS VARCHAR) AS "total_land_area",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-gfra-extent-of-forest"
