SELECT
    CAST("Country" AS VARCHAR) AS "Country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("position" AS VARCHAR) AS "position",
    CAST("Unit" AS VARCHAR) AS "Unit",
    CAST("value" AS VARCHAR) AS "value",
    CAST("wood_product" AS VARCHAR) AS "wood_product",
    CAST("Year" AS VARCHAR) AS "Year"
FROM "european-environment-agency-fise.v-countryfact-faostat-bioeco-wood-for-remov"
