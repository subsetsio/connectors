SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("order_col" AS VARCHAR) AS "order_col",
    CAST("patch_size" AS VARCHAR) AS "patch_size",
    CAST("percentage" AS VARCHAR) AS "percentage",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-clc-forest-patch-size-distribution"
