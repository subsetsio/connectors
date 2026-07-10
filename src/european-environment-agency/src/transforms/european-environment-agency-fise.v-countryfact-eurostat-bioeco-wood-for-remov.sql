SELECT
    CAST("bark" AS VARCHAR) AS "bark",
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("percentage_value" AS VARCHAR) AS "percentage_value",
    CAST("real_value" AS VARCHAR) AS "real_value",
    CAST("total" AS VARCHAR) AS "total",
    CAST("units" AS VARCHAR) AS "units",
    CAST("value" AS VARCHAR) AS "value",
    CAST("wood_product" AS VARCHAR) AS "wood_product",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-eurostat-bioeco-wood-for-remov"
