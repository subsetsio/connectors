SELECT
    CAST("Country_name" AS VARCHAR) AS "Country_name",
    CAST("forest" AS VARCHAR) AS "forest",
    CAST("GROWING STOCK DENSITY" AS VARCHAR) AS "GROWING STOCK DENSITY",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("Units" AS VARCHAR) AS "Units",
    CAST("volume" AS VARCHAR) AS "volume",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-growing-stock-density"
