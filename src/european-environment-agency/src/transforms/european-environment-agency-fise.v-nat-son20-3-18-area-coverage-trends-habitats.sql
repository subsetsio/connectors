SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("deteriorating" AS VARCHAR) AS "deteriorating",
    CAST("deteriorating_percentage" AS VARCHAR) AS "deteriorating_percentage",
    CAST("habitatgroup" AS VARCHAR) AS "habitatgroup",
    CAST("habitatgroup_with_total" AS VARCHAR) AS "habitatgroup_with_total",
    CAST("habitats" AS VARCHAR) AS "habitats",
    CAST("improving" AS VARCHAR) AS "improving",
    CAST("improving_percentage" AS VARCHAR) AS "improving_percentage",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("show_order" AS VARCHAR) AS "show_order",
    CAST("stable" AS VARCHAR) AS "stable",
    CAST("stable_percentage" AS VARCHAR) AS "stable_percentage",
    CAST("total" AS VARCHAR) AS "total",
    CAST("unknown" AS VARCHAR) AS "unknown",
    CAST("unknown_percentage" AS VARCHAR) AS "unknown_percentage"
FROM "european-environment-agency-fise.v-nat-son20-3-18-area-coverage-trends-habitats"
