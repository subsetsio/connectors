SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("species_occurring" AS VARCHAR) AS "species_occurring",
    CAST("value" AS VARCHAR) AS "value",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-biodiv-soef20-tree-species-occurring-unpivot"
