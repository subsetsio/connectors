SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("emissions" AS VARCHAR) AS "emissions",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("Pools" AS VARCHAR) AS "Pools",
    CAST("Units" AS VARCHAR) AS "Units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-gfra-clim-carbon-pools"
