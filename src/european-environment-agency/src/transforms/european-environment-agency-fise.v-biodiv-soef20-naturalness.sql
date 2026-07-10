SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("order_in_chart" AS VARCHAR) AS "order_in_chart",
    CAST("plantations" AS VARCHAR) AS "plantations",
    CAST("plantations_percentage" AS VARCHAR) AS "plantations_percentage",
    CAST("semi_natural" AS VARCHAR) AS "semi_natural",
    CAST("semi_natural_percentage" AS VARCHAR) AS "semi_natural_percentage",
    CAST("total" AS VARCHAR) AS "total",
    CAST("undisturbed_by_man" AS VARCHAR) AS "undisturbed_by_man",
    CAST("undisturbed_by_man_percentage" AS VARCHAR) AS "undisturbed_by_man_percentage",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-biodiv-soef20-naturalness"
