SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("forest_area_1000ha" AS VARCHAR) AS "forest_area_1000ha",
    CAST("number_species" AS VARCHAR) AS "number_species",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("sorting" AS VARCHAR) AS "sorting",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-biodiv-soef-4-1-1-forest-species"
