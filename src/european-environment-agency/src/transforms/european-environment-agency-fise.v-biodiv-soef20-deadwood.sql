SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("forest" AS VARCHAR) AS "forest",
    CAST("group_name" AS VARCHAR) AS "group_name",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("order_in_chart" AS VARCHAR) AS "order_in_chart",
    CAST("units" AS VARCHAR) AS "units",
    CAST("variable" AS VARCHAR) AS "variable",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-biodiv-soef20-deadwood"
